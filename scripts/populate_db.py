import os
import random
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import logging

logging.basicConfig(level=logging.INFO, format='%(levelname)-5.5s [%(name)s] %(message)s')
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.db.models import Base, Escola, Aluno, Professor

NOMES_ESCOLAS = [ "Escola Estadual Monteiro Lobato", "Colégio Aplicação", "Escola Municipal Machado de Assis", "Centro de Ensino Tiradentes", "Colégio Pedro II", "Escola Técnica Federal", "Instituto de Educação Anísio Teixeira", "Escola Estadual Santos Dumont", "Colégio Militar", "Escola de Referência", "Centro Educacional Vinícius de Moraes", "Escola Estadual Cecília Meireles", "Colégio Estadual Rui Barbosa", "Escola Municipal Clarice Lispector", "Instituto Federal de Educação", "Escola Estadual Graciliano Ramos", "Colégio Estadual Castro Alves", "Escola Municipal Zumbi dos Palmares", "Centro de Ensino Integral", "Escola Estadual Portinari", "Colégio Estadual Ayrton Senna", "Escola Municipal Cora Coralina", "Instituto Superior de Educação", "Escola Estadual Tarsila do Amaral", "Colégio Estadual Guimarães Rosa" ]
CIDADES_POR_REGIAO = { "Nordeste": ["Recife", "Salvador", "Fortaleza", "São Luís", "João Pessoa"], "Sudeste": ["São Paulo", "Rio de Janeiro", "Belo Horizonte", "Vitória", "Campinas"], "Sul": ["Porto Alegre", "Curitiba", "Florianópolis", "Caxias do Sul", "Joinville"], "Norte": ["Manaus", "Belém", "Porto Velho", "Boa Vista", "Palmas"], "Centro-Oeste": ["Brasília", "Goiânia", "Cuiabá", "Campo Grande", "Anápolis"] }

def populate_database(db_session):
    try:
        logging.info("Limpando dados antigos do banco de dados...")
        db_session.execute(text("TRUNCATE TABLE alunos, professores, escolas RESTART IDENTITY CASCADE;"))
        db_session.commit()

        logging.info("Populando o banco com dados históricos de 2015 a 2025...")
        ANO_INICIAL, ANO_FINAL = 2015, 2025
        ANO_INTERVENCAO = 2020
        escolas_cache = {}
        
        for ano in range(ANO_INICIAL, ANO_FINAL + 1):
            logging.info(f"-> Gerando dados para o ano de {ano}...")
            
            for i, nome_base in enumerate(NOMES_ESCOLAS):
                regiao = list(CIDADES_POR_REGIAO.keys())[i % 5]
                cidade = random.choice(CIDADES_POR_REGIAO[regiao])
                nome_completo = f"{nome_base} - {cidade}"
                
                pontuacao_anterior = escolas_cache.get(nome_completo, {}).get('pontuacao', round(random.uniform(5.0, 6.5), 2))
                avaliacao_prof_anterior = escolas_cache.get(nome_completo, {}).get('avaliacao_prof', round(random.uniform(6.0, 7.5), 2))

                if ano < ANO_INTERVENCAO:
                    flutuacao = round(random.uniform(-0.1, 0.12), 2)
                    pontuacao_escola = max(5.0, min(7.0, pontuacao_anterior + flutuacao))
                    flutuacao_prof = round(random.uniform(-0.15, 0.15), 2)
                    pontuacao_prof = max(5.5, min(8.0, avaliacao_prof_anterior + flutuacao_prof))
                else:
                    melhoria_escola = round(random.uniform(0.1, 0.4), 2)
                    pontuacao_escola = min(10.0, pontuacao_anterior + melhoria_escola)
                    melhoria_prof = round(random.uniform(0.1, 0.3), 2)
                    pontuacao_prof = min(10.0, avaliacao_prof_anterior + melhoria_prof)
                
                escola = Escola(
                    nome=nome_completo, regiao=regiao, pontuacao_premio=pontuacao_escola, 
                    ideb_publico=round(random.uniform(5.0, 7.5), 2), ano=ano
                )
                db_session.add(escola)
                db_session.flush()

                escolas_cache[nome_completo] = {'pontuacao': pontuacao_escola, 'avaliacao_prof': pontuacao_prof}

                alunos_para_adicionar = []
                for j in range(20):
                    nota_aluno = max(0, min(1000, pontuacao_escola * 100 + random.uniform(-50, 50)))
                    aluno = Aluno(
                        nome_anonimizado=f"Aluno {j+1}", nota_geral=round(nota_aluno, 2), 
                        escola_id=escola.id, ano=ano
                    )
                    alunos_para_adicionar.append(aluno)
                db_session.add_all(alunos_para_adicionar)

                professores_para_adicionar = []
                for k in range(5):
                    professor = Professor(
                        nome_anonimizado=f"Professor {k+1}", anos_experiencia=random.randint(2, 20),
                        pontuacao_avaliacao=round(pontuacao_prof, 2), escola_id=escola.id, ano=ano
                    )
                    professores_para_adicionar.append(professor)
                db_session.add_all(professores_para_adicionar)
            
            db_session.commit()
        
        logging.info("\nBanco de dados populado com sucesso!")

    except Exception as e:
        logging.error(f"\nOcorreu um erro durante a população: {e}")
        db_session.rollback()
    finally:
        db_session.close()

if __name__ == "__main__":
    load_dotenv()
    DATABASE_URL = os.getenv("DATABASE_URL")
    if not DATABASE_URL:
        logging.error("URL do banco de dados não encontrada. Verifique seu arquivo .env")
    else:
        logging.info("Conectando ao banco de dados...")
        engine = create_engine(DATABASE_URL)
        Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        db_session = Session()
        populate_database(db_session)