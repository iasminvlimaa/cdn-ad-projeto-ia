from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from app.api.endpoints import escolas, alunos

app = FastAPI(
    title="Dashboard do Prêmio de Educação - Instituto Alpargatas",
    description="Plataforma para análise de dados e impacto do Prêmio de Educação.",
    version="1.0.0"
)

# --- Configuração do Frontend ---
app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

# --- Endpoints da API (Backend) ---
app.include_router(escolas.router, prefix="/api")
app.include_router(alunos.router, prefix="/api")

# --- Endpoint para servir a página HTML (Frontend) ---
@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})