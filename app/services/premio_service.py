from sqlalchemy.orm import Session
from sqlalchemy import func, and_
from app.db import models

def apply_filters(query, ano: int, regiao: str):
    if ano:
        query = query.filter(models.Escola.ano == ano)
    if regiao and regiao != "Todas":
        query = query.filter(models.Escola.regiao == regiao)
    return query

def listar_escolas(db: Session, ano: int, regiao: str, nome: str = None):
    query = db.query(models.Escola)
    query = apply_filters(query, ano, regiao)
    if nome:
        query = query.filter(models.Escola.nome.contains(nome))
    return query.all()

def calcular_desempenho_geral(db: Session, ano: int, regiao: str):
    query = db.query(func.avg(models.Escola.pontuacao_premio))
    query = apply_filters(query, ano, regiao)
    media_geral = query.scalar()
    return {"media_geral_premio": round(media_geral, 2) if media_geral else 0}

def calcular_desempenho_por_regiao(db: Session, ano: int):
    query = db.query(
        models.Escola.regiao,
        func.avg(models.Escola.pontuacao_premio).label("media_pontuacao")
    )
    if ano:
        query = query.filter(models.Escola.ano == ano)
    query = query.group_by(models.Escola.regiao)
    resultado = query.all()
    return [{"regiao": r.regiao, "media_pontuacao": round(r.media_pontuacao, 2)} for r in resultado]

def listar_top_10_escolas(db: Session, ano: int, regiao: str):
    query = db.query(models.Escola)
    query = apply_filters(query, ano, regiao)
    return query.order_by(models.Escola.pontuacao_premio.desc()).limit(10).all()

def listar_top_10_alunos(db: Session, ano: int, regiao: str):
    query = db.query(models.Aluno).join(models.Escola)
    if ano:
        query = query.filter(models.Aluno.ano == ano)
    if regiao and regiao != "Todas":
        query = query.filter(models.Escola.regiao == regiao)
    return query.order_by(models.Aluno.nota_geral.desc()).limit(10).all()

def calcular_melhoria_anual(db: Session, ano: int, regiao: str):
    query_ano_atual = db.query(func.avg(models.Escola.pontuacao_premio))
    query_ano_anterior = db.query(func.avg(models.Escola.pontuacao_premio))
    media_atual = apply_filters(query_ano_atual, ano, regiao).scalar() or 0
    media_anterior = apply_filters(query_ano_anterior, ano - 1, regiao).scalar() or 0
    melhoria = ((media_atual - media_anterior) / media_anterior) * 100 if media_anterior else 0
    return {"melhoria_percentual": round(melhoria, 2)}

def calcular_benchmark_ideb(db: Session, ano: int, regiao: str):
    query = db.query(
        func.avg(models.Escola.pontuacao_premio).label("media_premio"),
        func.avg(models.Escola.ideb_publico).label("media_ideb")
    )
    query = apply_filters(query, ano, regiao)
    resultado = query.one_or_none()
    if not resultado: return {"diferenca_ideb": 0}
    media_premio = resultado.media_premio or 0
    media_ideb = resultado.media_ideb or 0
    diferenca = media_premio - media_ideb
    return {"diferenca_ideb": round(diferenca, 2)}

def obter_escolas_por_ids(db: Session, ids: list[int], ano: int):
    if not ids: return []
    return db.query(models.Escola).filter(models.Escola.id.in_(ids), models.Escola.ano == ano).all()

def obter_historico_escola(db: Session, escola_id: int):
    escola_ref = db.query(models.Escola).filter(models.Escola.id == escola_id).first()
    if not escola_ref: return []
    historico = db.query(
        models.Escola.ano,
        models.Escola.pontuacao_premio
    ).filter(models.Escola.nome == escola_ref.nome).order_by(models.Escola.ano).all()
    return [{"ano": h.ano, "pontuacao": h.pontuacao_premio} for h in historico]

def obter_jornada_escola(db: Session, escola_id: int):
    escola_ref = db.query(models.Escola).filter(models.Escola.id == escola_id).first()
    if not escola_ref: return None
    
    historico_completo = db.query(models.Escola).filter(
        models.Escola.nome == escola_ref.nome
    ).order_by(models.Escola.ano).all()
    if not historico_completo: return None

    primeiro_ano = historico_completo[0]
    ultimo_ano = historico_completo[-1]
    
    crescimento = 0
    if primeiro_ano.pontuacao_premio > 0:
        crescimento = ((ultimo_ano.pontuacao_premio - primeiro_ano.pontuacao_premio) / primeiro_ano.pontuacao_premio) * 100

    melhor_registro = max(historico_completo, key=lambda x: x.pontuacao_premio)
    
    total_alunos_destaque = db.query(func.count(models.Aluno.id)).join(models.Escola).filter(
        models.Escola.nome == escola_ref.nome
    ).scalar()

    kpis = {
        "crescimento_total_percentual": round(crescimento, 1),
        "melhor_ano": melhor_registro.ano,
        "melhor_pontuacao": melhor_registro.pontuacao_premio,
        "total_alunos_destaque": total_alunos_destaque or 0
    }

    historico_jornada = []
    for registro_anual in historico_completo:
        escolas_do_ano_na_regiao = db.query(models.Escola.id).filter(
            and_(models.Escola.ano == registro_anual.ano, models.Escola.regiao == registro_anual.regiao)
        ).order_by(models.Escola.pontuacao_premio.desc()).all()
        
        ids_ordenadas = [escola.id for escola in escolas_do_ano_na_regiao]
        try:
            ranking = ids_ordenadas.index(registro_anual.id) + 1
        except ValueError:
            ranking = None 
        
        historico_jornada.append({
            "ano": registro_anual.ano,
            "pontuacao": registro_anual.pontuacao_premio,
            "ranking_regional": ranking
        })

    return {"kpis": kpis, "historico_jornada": historico_jornada}

def calcular_impacto_escolas_e_alunos(db: Session, escola_ids: List[int], ano_antes: int, ano_depois: int):
    escolas_selecionadas = db.query(models.Escola).filter(models.Escola.id.in_(escola_ids)).all()
    nomes_escolas_unicas = sorted(list(set([e.nome for e in escolas_selecionadas])))

    impacto_escolas_data = []
    for nome in nomes_escolas_unicas:
        pontuacao_antes = db.query(models.Escola.pontuacao_premio).filter(
            models.Escola.nome == nome, models.Escola.ano == ano_antes
        ).scalar()
        pontuacao_depois = db.query(models.Escola.pontuacao_premio).filter(
            models.Escola.nome == nome, models.Escola.ano == ano_depois
        ).scalar()
        impacto_escolas_data.append({
            "nome_escola": nome,
            "pontuacao_antes": pontuacao_antes,
            "pontuacao_depois": pontuacao_depois
        })

    ids_escolas_antes = [e.id for e in db.query(models.Escola.id).filter(models.Escola.nome.in_(nomes_escolas_unicas), models.Escola.ano == ano_antes).all()]
    ids_escolas_depois = [e.id for e in db.query(models.Escola.id).filter(models.Escola.nome.in_(nomes_escolas_unicas), models.Escola.ano == ano_depois).all()]
    
    media_alunos_antes = db.query(func.avg(models.Aluno.nota_geral)).filter(
        models.Aluno.escola_id.in_(ids_escolas_antes)
    ).scalar()
    media_alunos_depois = db.query(func.avg(models.Aluno.nota_geral)).filter(
        models.Aluno.escola_id.in_(ids_escolas_depois)
    ).scalar()

    impacto_alunos_data = {
        "media_alunos_antes": media_alunos_antes,
        "media_alunos_depois": media_alunos_depois
    }

    return {"escolas": impacto_escolas_data, "alunos": impacto_alunos_data}