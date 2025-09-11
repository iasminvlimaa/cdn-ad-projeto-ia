from pydantic import BaseModel
from typing import List

class AlunoBase(BaseModel):
    nome_anonimizado: str
    nota_geral: float
    ano: int

class AlunoInDB(AlunoBase):
    id: int
    escola_id: int
    class Config:
        from_attributes = True

class EscolaBase(BaseModel):
    nome: str
    regiao: str
    pontuacao_premio: float
    ideb_publico: float
    ano: int

class EscolaInDB(EscolaBase):
    id: int
    alunos: List[AlunoInDB] = []
    class Config:
        from_attributes = True

class DesempenhoRegiao(BaseModel):
    regiao: str
    media_pontuacao: float

class HistoricoPonto(BaseModel):
    ano: int
    pontuacao: float