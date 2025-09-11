from sqlalchemy.orm import Session
from sqlalchemy import func
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