from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from app.api.endpoints import escolas, alunos
from app.initial_data import init_db # <-- 1. IMPORTAR A NOVA FUNÇÃO
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Código a ser executado na inicialização
    print("--- INICIANDO APLICAÇÃO ---")
    init_db() # <-- 2. CHAMAR A FUNÇÃO DE INICIALIZAÇÃO
    print("--- APLICAÇÃO INICIADA ---")
    yield
    # Código a ser executado no desligamento (não usaremos aqui)

# --- 3. ADICIONAR O LIFESPAN AO APP ---
app = FastAPI(
    title="Dashboard do Prêmio de Educação - Instituto Alpargatas",
    description="Plataforma para análise de dados e impacto do Prêmio de Educação.",
    version="1.0.0",
    lifespan=lifespan
)

app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

app.include_router(escolas.router, prefix="/api")
app.include_router(alunos.router, prefix="/api")

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})