from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.api import deps

router = APIRouter()

@router.get("/debug/count-escolas", tags=["Debug"])
def count_escolas_in_db(db: Session = Depends(deps.get_db)):
    """
    Endpoint de diagnóstico para contar o número de registros na tabela 'escolas'.
    Isso nos ajuda a verificar se a população de dados funcionou.
    """
    try:
        # Executa uma consulta SQL simples para contar as linhas
        query = text("SELECT COUNT(*) FROM escolas;")
        count = db.execute(query).scalar_one()
        return {"tabela": "escolas", "registros_encontrados": count}
    except Exception as e:
        # Se a tabela não existir, a exceção será capturada
        return {"erro": f"Não foi possível consultar a tabela 'escolas'.", "detalhe": str(e)}