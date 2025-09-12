from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

# Importa todos os "roteadores" que contêm nossos endpoints
from app.api.endpoints import escolas, alunos, setup, debug # <-- 1. IMPORTAR O DEBUG

app = FastAPI(
    title="Dashboard do Prêmio de Educação - Instituto Alpargatas",
    description="Plataforma para análise de dados e impacto do Prêmio de Educação.",
    version="1.0.0"
)

# ... (app.mount e templates continuam os mesmos) ...

# Inclui os endpoints da sua API no aplicativo principal
app.include_router(escolas.router, prefix="/api")
app.include_router(alunos.router, prefix="/api")
app.include_router(setup.router, prefix="/api")
app.include_router(debug.router, prefix="/api") # <-- 2. ADICIONAR A ROTA DE DEBUG

# Endpoint principal que serve a página do dashboard
@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})