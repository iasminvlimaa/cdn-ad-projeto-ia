import os
import random
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import logging

# Configuração básica de logging
logging.basicConfig(level=logging.INFO, format='%(levelname)-5.5s [%(name)s] %(message)s')

# Adicionado para permitir importação da app
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.db.models import Base, Escola, Aluno

# Listas de Dados Mocados
NOMES_ESCOLAS = [ "Escola Estadual Monteiro Lobato", "Colégio Aplicação", "Escola Municipal Machado de Assis", "Centro de Ensino Tiradentes", "Colégio Pedro II", "Escola Técnica Federal", "Instituto de Educação Anísio Teixeira", "Escola Estadual Santos Dumont", "Colégio Militar", "Escola de Referência", "Centro Educacional Vinícius de Moraes", "Escola Estadual Cecília Meireles", "Colégio Estadual Rui Barbosa", "Escola Municipal Clarice Lispector", "Instituto Federal de Educação", "Escola Estadual Graciliano Ramos", "Colégio Estadual Castro Alves", "Escola Municipal Zumbi dos Palmares", "Centro de Ensino Integral", "Escola Estadual Portinari", "Colégio Estadual Ayrton Senna", "Escola Municipal Cora Coralina", "Instituto Superior de Educação", "Escola Estadual Tarsila do Amaral", "Colégio Estadual Guimarães Rosa" ]
CIDADES_POR_REGIAO = { "Nordeste": ["Recife", "Salvador", "Fortaleza", "São Luís", "João Pessoa"], "Sudeste": ["São Paulo", "Rio de Janeiro", "Belo Horizonte", "Vitória", "Campinas"], "Sul": ["Porto Alegre", "Curitiba", "Florianópolis", "Caxias do Sul", "Joinville"], "Norte": ["Manaus", "Belém", "Porto Velho", "Boa Vista", "Palmas"], "Centro-Oeste": ["Brasília", "Goiânia", "Cuiabá", "Campo Grande", "Anápolis"] }

def populate_database(db_session):
    try:
        logging.info("Limpando dados antigos do banco de dados...")
        db_session.execute(text("TRUNCATE TABLE alunos, escolas RESTART IDENTITY CASCADE;"))
        db_session.commit()

        logging.info("Populando o banco de dados com dados históricos de 2015 a 2025...")
        ANO_INICIAL, ANO_FINAL = 2015, 2025
        ANO_INTERVENCAO = 2020 # Ano em que o "impacto" começa
        escolas_cache = {}
        
        for ano in range(ANO_INICIAL, ANO_FINAL + 1):
            logging.info(f"-> Gerando dados para o ano de {ano}...")
            escolas_neste_ano = []
            for i, nome_base in enumerate(NOMES_ESCOLAS):
                regiao = list(CIDADES_POR_REGIAO.keys())[i % 5]
                cidade = random.choice(CIDADES_POR_REGIAO[regiao])
                nome = f"{nome_base} - {cidade}"
                
                pontuacao_anterior = escolas_cache.get(nome)

                if pontuacao_anterior is None:
                    pontuacao_anterior = round(random.uniform(5.0, 6.5), 2)

                if ano < ANO_INTERVENCAO:
                    flutuacao = round(random.uniform(-0.1, 0.12), 2)
                    pontuacao = max(5.0, min(7.0, pontuacao_anterior + flutuacao))
                else:
                    melhoria = round(random.uniform(0.1, 0.4), 2)
                    pontuacao = min(10.0, pontuacao_anterior + melhoria)
                
                ideb = round(random.uniform(5.0, 7.5), 2)
                escola = Escola(nome=nome, regiao=regiao, pontuacao_premio=pontuacao, ideb_publico=ideb, ano=ano)
                escolas_neste_ano.append(escola)
                escolas_cache[nome] = pontuacao
            
            db_session.add_all(escolas_neste_ano)
            db_session.commit()

            if ano == ANO_FINAL:
                logging.info(f"   -> Gerando 100 alunos destaques para {ano}...")
                for _ in range(100):
                    escola = random.choice(escolas_neste_ano)
                    nota_aluno = round(random.uniform(escola.pontuacao_premio * 80, escola.pontuacao_premio * 105), 2)
                    aluno = Aluno(nome_anonimizado=f"Aluno Destaque {_ + 1}", nota_geral=nota_aluno, escola_id=escola.id, ano=ano)
                    db_session.add(aluno)
                db_session.commit()
        
        logging.info(f"\nBanco de dados populado com sucesso! Total de {len(NOMES_ESCOLAS) * (ANO_FINAL - ANO_INICIAL + 1)} registros de escolas.")

    except Exception as e:
        logging.error(f"\nOcorreu um erro durante a população: {e}")
        db_session.rollback()
    finally:
        db_session.close()

if __name__ == "__main__":
    load_dotenv()
    DATABASE_URL = os.getenv("DATABASE_URL") or os.getenv("EXTERNAL_DB_URL")
    if not DATABASE_URL:
        logging.error("URL do banco de dados não encontrada. Verifique seu arquivo .env")
    else:
        logging.info("Conectando ao banco de dados...")
        engine = create_engine(DATABASE_URL)
        Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        db_session = Session()
        populate_database(db_session)