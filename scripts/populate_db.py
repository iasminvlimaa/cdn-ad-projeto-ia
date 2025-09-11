from app.db.session import SessionLocal
from app.db.models import Escola, Aluno
from sqlalchemy import text
import random

NOMES_ESCOLAS = [ "Escola Estadual Monteiro Lobato", "Colégio Aplicação", "Escola Municipal Machado de Assis", "Centro de Ensino Tiradentes", "Colégio Pedro II", "Escola Técnica Federal", "Instituto de Educação Anísio Teixeira", "Escola Estadual Santos Dumont", "Colégio Militar", "Escola de Referência", "Centro Educacional Vinícius de Moraes", "Escola Estadual Cecília Meireles", "Colégio Estadual Rui Barbosa", "Escola Municipal Clarice Lispector", "Instituto Federal de Educação", "Escola Estadual Graciliano Ramos", "Colégio Estadual Castro Alves", "Escola Municipal Zumbi dos Palmares", "Centro de Ensino Integral", "Escola Estadual Portinari", "Colégio Estadual Ayrton Senna", "Escola Municipal Cora Coralina", "Instituto Superior de Educação", "Escola Estadual Tarsila do Amaral", "Colégio Estadual Guimarães Rosa" ]
CIDADES_POR_REGIAO = { "Nordeste": ["Recife", "Salvador", "Fortaleza", "São Luís", "João Pessoa"], "Sudeste": ["São Paulo", "Rio de Janeiro", "Belo Horizonte", "Vitória", "Campinas"], "Sul": ["Porto Alegre", "Curitiba", "Florianópolis", "Caxias do Sul", "Joinville"], "Norte": ["Manaus", "Belém", "Porto Velho", "Boa Vista", "Palmas"], "Centro-Oeste": ["Brasília", "Goiânia", "Cuiabá", "Campo Grande", "Anápolis"] }

def populate_database():
    db = SessionLocal()
    try:
        print("Limpando dados antigos...")
        db.execute(text("TRUNCATE TABLE public.alunos, public.escolas RESTART IDENTITY CASCADE;"))
        db.commit()

        print("Populando com dados históricos de 2020 a 2025...")
        ANO_INICIAL, ANO_FINAL = 2020, 2025
        escolas_cache = {}
        
        for ano in range(ANO_INICIAL, ANO_FINAL + 1):
            print(f"-> Gerando dados para {ano}...")
            escolas_neste_ano = []
            for i, nome_base in enumerate(NOMES_ESCOLAS):
                regiao = list(CIDADES_POR_REGIAO.keys())[i % 5]
                cidade = random.choice(CIDADES_POR_REGIAO[regiao])
                nome = f"{nome_base} - {cidade}"
                pontuacao_anterior = escolas_cache.get(nome, round(random.uniform(5.0, 7.0), 2))
                melhoria = round(random.uniform(0.1, 0.4), 2) if ano > ANO_INICIAL else 0
                pontuacao = min(10.0, pontuacao_anterior + melhoria)
                ideb = round(random.uniform(5.0, 7.5), 2)
                escola = Escola(nome=nome, regiao=regiao, pontuacao_premio=pontuacao, ideb_publico=ideb, ano=ano)
                escolas_neste_ano.append(escola)
                escolas_cache[nome] = pontuacao
            
            db.add_all(escolas_neste_ano)
            db.commit() # Salva as escolas para obter os IDs

            # --- MUDANÇA PRINCIPAL: CRIA ALUNOS PARA CADA ANO ---
            print(f"   -> Gerando 20 alunos destaques para {ano}...")
            for _ in range(20): # Vamos criar 20 alunos por ano
                escola = random.choice(escolas_neste_ano)
                nota_base = escola.pontuacao_premio
                # Gera notas altas para serem "destaques"
                nota_aluno = round(random.uniform(nota_base * 90, nota_base * 110), 2)
                if nota_aluno > 1000: nota_aluno = 1000.0
                aluno = Aluno(nome_anonimizado=f"Aluno Destaque {_ + 1}", nota_geral=nota_aluno, escola_id=escola.id, ano=ano)
                db.add(aluno)
            db.commit()
        
        print(f"\nBanco populado! Total de {len(NOMES_ESCOLAS) * (ANO_FINAL - ANO_INICIAL + 1)} registros de escolas.")

    except Exception as e:
        print(f"\nErro: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    populate_database()