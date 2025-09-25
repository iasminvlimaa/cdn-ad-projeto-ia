from pydantic import BaseModel, Field
from typing import List, Optional

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
    latitude: Optional[float] = None
    longitude: Optional[float] = None

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

class JornadaKPIs(BaseModel):
    crescimento_total_percentual: float = Field(..., description="Crescimento percentual da nota do primeiro ao último ano.")
    melhor_ano: int = Field(..., description="Ano com a maior pontuação registrada.")
    melhor_pontuacao: float = Field(..., description="A maior pontuação registrada.")
    total_alunos_destaque: int = Field(..., description="Número total de alunos destaque da escola em todos os anos.")

class PontoDaJornada(BaseModel):
    ano: int
    pontuacao: float
    ranking_regional: Optional[int] = Field(..., description="Posição da escola no ranking da sua região naquele ano.")

class JornadaEscolaResponse(BaseModel):
    kpis: JornadaKPIs
    historico_jornada: List[PontoDaJornada]

class ImpactoEscolaData(BaseModel):
    nome_escola: str
    pontuacao_antes: Optional[float] = None
    pontuacao_depois: Optional[float] = None

class ImpactoAlunosData(BaseModel):
    media_alunos_antes: Optional[float] = None
    media_alunos_depois: Optional[float] = None

class ImpactoEscolasResponse(BaseModel):
    escolas: List[ImpactoEscolaData]
    alunos: ImpactoAlunosData

class ImpactoRequest(BaseModel):
    escola_ids: List[int]
    ano_depois: int
    ano_antes: int = 2019