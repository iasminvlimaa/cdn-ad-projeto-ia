from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.api import deps
from app.services import premio_service
from app.schemas import premio

router = APIRouter()

@router.get("/alunos/destaques", response_model=List[premio.AlunoInDB], tags=["Rankings"])
def get_alunos_destaques(ano: int, regiao: str, db: Session = Depends(deps.get_db)):
    return premio_service.listar_top_10_alunos(db=db, ano=ano, regiao=regiao)