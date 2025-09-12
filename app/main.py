from fastapi import FastAPI, Request, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from sqlalchemy import text

# Importa os roteadores que contêm nossos endpoints
from app.api.endpoints import escolas, alunos, setup
from app.api import deps # Importa a dependência do banco

app = FastAPI(
    title="Dashboard do Prêmio de Educação - Instituto Alpargatas",
    description="Plataforma para análise de dados e impacto do Prêmio de Educação.",
    version="1.0.0"
)

# Configura a pasta "static" para servir arquivos CSS, JS, etc.
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Configura a pasta "templates" para servir o arquivo HTML
templates = Jinja2Templates(directory="app/templates")

# Inclui os endpoints da sua API no aplicativo principal
app.include_router(escolas.router, prefix="/api")
app.include_router(alunos.router, prefix="/api")
app.include_router(setup.router, prefix="/api")

# --- NOVO ENDPOINT DE DEBUG ADICIONADO DIRETAMENTE AQUI ---
@app.get("/api/debug/count_escolas", tags=["Debug"])
def count_escolas_in_db(db: Session = Depends(deps.get_db)):
    """
    Endpoint de diagnóstico para contar o número de registros na tabela 'escolas'.
    """
    try:
        query = text("SELECT COUNT(*) FROM escolas;")
        count = db.execute(query).scalar_one()
        return {"tabela": "escolas", "registros_encontrados": count}
    except Exception as e:
        return {"erro": "Não foi possível consultar a tabela 'escolas'.", "detalhe": str(e)}

# Endpoint principal que serve a página do dashboard
@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    """
    Carrega a interface do usuário (frontend) do dashboard.
    """
    return templates.TemplateResponse("index.html", {"request": request})