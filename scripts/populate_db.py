import os
import random
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# --- Definição dos Modelos do Banco (Copiado de app/db/models.py) ---
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import Column, Integer, String, Float, ForeignKey
Base = declarative_base()

class Escola(Base):
    __tablename__ = "escolas"
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, index=True)
    regiao = Column(String)
    pontuacao_premio = Column(Float)
    ideb_publico = Column(Float)
    ano = Column(Integer, index=True)
    alunos = relationship("Aluno", back_populates="escola")

class Aluno(Base):
    __tablename__ = "alunos"
    id = Column(Integer, primary_key=True, index=True)
    nome_anonimizado = Column(String)
    nota_geral = Column(Float)
    escola_id = Column(Integer, ForeignKey("escolas.id"))
    ano = Column(Integer, index=True)
    escola = relationship("Escola", back_populates="alunos")

# --- Listas de Dados Mocados ---
NOMES_ESCOLAS = [ "Escola Estadual Monteiro Lobato", "Colégio Aplicação", "Escola Municipal Machado de Assis", "Centro de Ensino Tiradentes", "Colégio Pedro II", "Escola Técnica Federal", "Instituto de Educação Anísio Teixeira", "Escola Estadual Santos Dumont", "Colégio Militar", "Escola de Referência", "Centro Educacional Vinícius de Moraes", "Escola Estadual Cecília Meireles", "Colégio Estadual Rui Barbosa", "Escola Municipal Clarice Lispector", "Instituto Federal de Educação", "Escola Estadual Graciliano Ramos", "Colégio Estadual Castro Alves", "Escola Municipal Zumbi dos Palmares", "Centro de Ensino Integral", "Escola Estadual Portinari", "Colégio Estadual Ayrton Senna", "Escola Municipal Cora Coralina", "Instituto Superior de Educação", "Escola Estadual Tarsila do Amaral", "Colégio Estadual Guimarães Rosa" ]
CIDADES_POR_REGIAO = { "Nordeste": ["Recife", "Salvador", "Fortaleza", "São Luís", "João Pessoa"], "Sudeste": ["São Paulo", "Rio de Janeiro", "Belo Horizonte", "Vitória", "Campinas"], "Sul": ["Porto Alegre", "Curitiba", "Florianópolis", "Caxias do Sul", "Joinville"], "Norte": ["Manaus", "Belém", "Porto Velho", "Boa Vista", "Palmas"], "Centro-Oeste": ["Brasília", "Goiânia", "Cuiabá", "Campo Grande", "Anápolis"] }


def populate_database(db_session):
    """Função principal que popula o banco de dados usando a sessão fornecida."""
    try:
        print("Limpando dados antigos do banco de dados...")
        db_session.execute(text("TRUNCATE TABLE public.alunos, public.escolas RESTART IDENTITY CASCADE;"))
        db_session.commit()

        print("Populando o banco de dados com dados históricos de 2020 a 2025...")
        ANO_INICIAL, ANO_FINAL = 2020, 2025
        escolas_cache = {}
        
        for ano in range(ANO_INICIAL, ANO_FINAL + 1):
            print(f"-> Gerando dados para o ano de {ano}...")
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
            
            db_session.add_all(escolas_neste_ano)
            db_session.commit()

            if ano == ANO_FINAL:
                print(f"   -> Gerando 100 alunos destaques para {ano}...")
                for _ in range(100):
                    escola = random.choice(escolas_neste_ano)
                    nota_aluno = round(random.uniform(escola.pontuacao_premio * 80, escola.pontuacao_premio * 105), 2)
                    aluno = Aluno(nome_anonimizado=f"Aluno Destaque {_ + 1}", nota_geral=nota_aluno, escola_id=escola.id, ano=ano)
                    db_session.add(aluno)
                db_session.commit()
        
        print(f"\nBanco de dados populado com sucesso! Total de {len(NOMES_ESCOLAS) * (ANO_FINAL - ANO_INICIAL + 1)} registros de escolas.")

    except Exception as e:
        print(f"\nOcorreu um erro durante a população: {e}")
        db_session.rollback()
    finally:
        db_session.close()

# --- Bloco de Execução Principal ---
if __name__ == "__main__":
    load_dotenv()
    
    DATABASE_URL = os.getenv("EXTERNAL_DB_URL") # Usando a URL externa do Render

    if not DATABASE_URL:
        print("!!! ERRO !!!")
        print("Certifique-se de que seu arquivo .env contém a linha:")
        print('EXTERNAL_DB_URL="SUA_URL_EXTERNA_DO_RENDER_AQUI"')
    else:
        print("Conectando ao banco de dados externo...")
        engine = create_engine(DATABASE_URL)
        Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        db_session = Session()
        
        populate_database(db_session)