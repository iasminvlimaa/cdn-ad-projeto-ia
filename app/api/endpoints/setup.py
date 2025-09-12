from fastapi import APIRouter, HTTPException
from app.initial_data import init_db

router = APIRouter()

@router.post("/setup-database", tags=["Setup"])
def setup_database():
    """
    Endpoint SECRETO para configurar o banco de dados.
    Roda as migrações e popula os dados.
    """
    try:
        print("--- ACIONANDO SETUP MANUAL DO BANCO DE DADOS ---")
        init_db()
        return {"message": "Banco de dados configurado com sucesso!"}
    except Exception as e:
        print(f"Erro no setup manual: {e}")
        raise HTTPException(status_code=500, detail=str(e))