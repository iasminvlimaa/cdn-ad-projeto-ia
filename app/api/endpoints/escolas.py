from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from app.api import deps
from app.services import premio_service
from app.schemas import premio

router = APIRouter()

@router.get("/escolas", response_model=List[premio.EscolaInDB], tags=["Escolas"])
def get_escolas(ano: int, regiao: str, nome: Optional[str] = Query(None), db: Session = Depends(deps.get_db)):
    return premio_service.listar_escolas(db=db, ano=ano, regiao=regiao, nome=nome)

@router.get("/desempenho/geral", tags=["Desempenho"])
def get_desempenho_geral(ano: int, regiao: str, db: Session = Depends(deps.get_db)):
    return premio_service.calcular_desempenho_geral(db=db, ano=ano, regiao=regiao)

@router.get("/desempenho/regioes", response_model=List[premio.DesempenhoRegiao], tags=["Desempenho"])
def get_desempenho_por_regiao(ano: int, db: Session = Depends(deps.get_db)):
    return premio_service.calcular_desempenho_por_regiao(db=db, ano=ano)

@router.get("/escolas/top10", response_model=List[premio.EscolaInDB], tags=["Rankings"])
def get_top_10_escolas(ano: int, regiao: str, db: Session = Depends(deps.get_db)):
    return premio_service.listar_top_10_escolas(db=db, ano=ano, regiao=regiao)

@router.get("/desempenho/melhoria-anual", tags=["Desempenho"])
def get_melhoria_anual(ano: int, regiao: str, db: Session = Depends(deps.get_db)):
    return premio_service.calcular_melhoria_anual(db=db, ano=ano, regiao=regiao)

@router.get("/desempenho/benchmark-ideb", tags=["Desempenho"])
def get_benchmark_ideb(ano: int, regiao: str, db: Session = Depends(deps.get_db)):
    return premio_service.calcular_benchmark_ideb(db=db, ano=ano, regiao=regiao)

@router.post("/escolas/comparar", response_model=List[premio.EscolaInDB], tags=["Análises"])
def get_escolas_para_comparacao(escola_ids: List[int], ano: int, db: Session = Depends(deps.get_db)):
    return premio_service.obter_escolas_por_ids(db=db, ids=escola_ids, ano=ano)

@router.get("/escolas/{escola_id}/historico", response_model=List[premio.HistoricoPonto], tags=["Análises"])
def get_historico_escola(escola_id: int, db: Session = Depends(deps.get_db)):
    return premio_service.obter_historico_escola(db=db, escola_id=escola_id)

@router.get("/escolas/{escola_id}/jornada", response_model=premio.JornadaEscolaResponse, tags=["Análises"])
def get_jornada_escola(escola_id: int, db: Session = Depends(deps.get_db)):
    jornada_data = premio_service.obter_jornada_escola(db=db, escola_id=escola_id)
    if not jornada_data:
        raise HTTPException(status_code=404, detail="Dados da jornada não encontrados para a escola")
    return jornada_data

@router.post("/impacto", response_model=premio.ImpactoResponse, tags=["Impacto"])
def get_analise_de_impacto(payload: premio.ImpactoRequest, db: Session = Depends(deps.get_db)):
    return premio_service.calcular_impacto_escolas_e_alunos(
        db=db, 
        escola_ids=payload.escola_ids, 
        ano_antes=payload.ano_antes, 
        ano_depois=payload.ano_depois
    )