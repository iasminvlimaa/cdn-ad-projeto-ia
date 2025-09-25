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

class ProfessorBase(BaseModel):
    nome_anonimizado: str
    anos_experiencia: int
    pontuacao_avaliacao: float
    ano: int

class ProfessorInDB(ProfessorBase):
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
    # AO COMENTAR AS LINHAS ABAIXO, SIMPLIFICAMOS A RESPOSTA DA API PARA RESOLVER O ERRO
    # alunos: List[AlunoInDB] = []
    # professores: List[ProfessorInDB] = []
    class Config:
        from_attributes = True

class DesempenhoRegiao(BaseModel):
    regiao: str
    media_pontuacao: float

class HistoricoPonto(BaseModel):
    ano: int
    pontuacao: float

class JornadaKPIs(BaseModel):
    crescimento_total_percentual: float
    melhor_ano: int
    melhor_pontuacao: float
    total_alunos_destaque: int

class PontoDaJornada(BaseModel):
    ano: int
    pontuacao: float
    ranking_regional: Optional[int]

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

class ImpactoProfessoresData(BaseModel):
    media_professores_antes: Optional[float] = None
    media_professores_depois: Optional[float] = None

class ImpactoResponse(BaseModel):
    escolas: List[ImpactoEscolaData]
    alunos: ImpactoAlunosData
    professores: ImpactoProfessoresData

class ImpactoRequest(BaseModel):
    escola_ids: List[int]
    ano_depois: int
    ano_antes: int = 2019