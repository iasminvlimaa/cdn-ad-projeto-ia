from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base

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