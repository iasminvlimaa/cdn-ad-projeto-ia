# Dashboard de Análise de Impacto - Prêmio de Educação

[![Live Demo](https://img.shields.io/badge/Ver_Demo-Online-brightgreen)](https://cdn-ad-projeto-ia.onrender.com)

## 📖 Sobre o Projeto

Este projeto é uma aplicação web full-stack desenvolvida como objeto avaliativo para a matéria de Análise de Dados. O objetivo é criar uma ferramenta interativa para analisar e visualizar o impacto do "Prêmio de Educação" do Instituto Alpargatas no desempenho de escolas, alunos e professores ao longo de um período de 11 anos (2015-2025).

A plataforma utiliza um backend robusto em **FastAPI** para processar e servir os dados, e um frontend dinâmico em **Vanilla JavaScript** para criar uma experiência de usuário rica e interativa, com visualizações de dados geradas pela biblioteca **Chart.js**.

**Link para a aplicação:** [https://cdn-ad-projeto-ia.onrender.com](https://cdn-ad-projeto-ia.onrender.com)

## ✨ Funcionalidades Principais

* **Dashboard Geral:** Visão de alto nível com KPIs (Média Geral, Melhoria Anual, Benchmark vs. IDEB), gráfico de desempenho por região e rankings de Top 10 escolas e alunos.
* **Análises Detalhadas:**
    * **Jornada da Escola:** Um mergulho profundo na evolução histórica de uma única escola, com gráfico de progressão, KPIs de impacto e uma linha do tempo de conquistas.
    * **Comparativo de Escolas:** Ferramenta para comparar lado a lado os indicadores de até 3 escolas diferentes.
* **Análise de Impacto:** A principal funcionalidade do projeto. Compara o desempenho de escolas, alunos e professores em um cenário "Antes" (ano base de 2019) vs. "Depois" (2020-2025), medindo o impacto real da intervenção.
* **Relatórios e Exportação:** Tabela com todos os dados filtrados e funcionalidade para exportar os resultados em formato `.csv`.
* **Interface Moderna:** Design responsivo que se adapta a dispositivos móveis, com menu retrátil e um seletor de tema (claro/escuro).

## 🛠️ Tecnologias Utilizadas

* **Backend:**
    * Python 3.13
    * FastAPI
    * SQLAlchemy (ORM)
    * Alembic (Migrações de Banco de Dados)
    * Pydantic (Validação de Dados)
    * Gunicorn & Uvicorn (Servidor de Aplicação)

* **Frontend:**
    * HTML5
    * CSS3
    * Vanilla JavaScript (SPA - Single Page Application)
    * Chart.js (Visualização de Dados)

* **Banco de Dados:**
    * PostgreSQL

* **Implantação (Deploy):**
    * Render

## 📸 Screenshots

### **Dashboard Principal**
![Dashboard Principal](https://github.com/iasminvlimaa/cdn-ad-projeto-ia/blob/main/images/dashboard_principal.png?raw=true)

### **Análises Detalhadas e de Impacto**
| Jornada da Escola (Evolução) | Análise de Impacto (Antes/Depois) | Comparativo de Escolas |
| :---: | :---: | :---: 
| ![Jornada da Escola](https://github.com/iasminvlimaa/cdn-ad-projeto-ia/blob/main/images/analises_2.png?raw=true) | ![Impacto nas Escolas](https://github.com/iasminvlimaa/cdn-ad-projeto-ia/blob/main/images/impactos_1.png?raw=true) | ![Comparativo de Escolas](https://github.com/iasminvlimaa/cdn-ad-projeto-ia/blob/main/images/analises_1.png?raw=true) |
| ![Histórico](https://github.com/iasminvlimaa/cdn-ad-projeto-ia/blob/main/images/analises_3.png?raw=true) | ![Impactos nos Alunos e nos Professores](https://github.com/iasminvlimaa/cdn-ad-projeto-ia/blob/main/images/impactos_2.png?raw=true)


### **Outras Telas**
| Relatórios e Exportação| 
| :---: |
| ![Tela de Relatórios](https://github.com/iasminvlimaa/cdn-ad-projeto-ia/blob/main/images/relatorios.png?raw=true) |

## 📂 Estrutura do Projeto

A arquitetura do projeto segue as melhores práticas de separação de responsabilidades:
```
/
├── alembic/              # Configuração e scripts de migração do banco de dados
│   └── versions/
├── app/
│   ├── api/              # Lógica da API (endpoints e dependências)
│   │   └── endpoints/
│   ├── core/             # Configurações centrais da aplicação
│   ├── db/               # Modelos SQLAlchemy e lógica de sessão
│   ├── schemas/          # Modelos Pydantic para validação
│   ├── services/         # Lógica de negócio e consultas ao banco
│   ├── static/           # Arquivos de frontend (CSS, JS)
│   └── templates/        # Arquivo principal index.html
├── scripts/              # Scripts de utilidade (ex: popular o banco)
├── .env                  # Arquivo para variáveis de ambiente (não versionado)
├── alembic.ini           # Arquivo de configuração do Alembic
├── Procfile              # Comando para iniciar a aplicação na Render
└── requirements.txt      # Dependências Python do projeto
```

## 🚀 Como Executar Localmente

Siga os passos abaixo para configurar e executar o projeto na sua máquina.

### Pré-requisitos
* Python 3.9+
* PostgreSQL instalado e rodando.
* Git

### Instalação
1.  **Clone o repositório:**
    ```bash
    git clone [https://github.com/iasminvlimaa/cdn-ad-projeto-ia.git](https://github.com/iasminvlimaa/cdn-ad-projeto-ia.git)
    cd cdn-ad-projeto-ia
    ```

2.  **Crie e ative um ambiente virtual:**
    ```bash
    # Windows
    python -m venv venv
    .\venv\Scripts\activate

    # macOS / Linux
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Instale as dependências:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure o Banco de Dados:**
    * Crie um banco de dados no PostgreSQL (ex: `projeto_alpargatas_db`).
    * Crie um arquivo chamado `.env` na raiz do projeto.
    * Adicione a URL de conexão do seu banco de dados local ao arquivo `.env`:
        ```
        DATABASE_URL="postgresql://SEU_USUARIO:SUA_SENHA@localhost:5432/projeto_alpargatas_db"
        ```

5.  **Crie as Tabelas (Migração):**
    * O Alembic irá ler a `DATABASE_URL` do `.env` e criar todas as tabelas necessárias.
    ```bash
    alembic upgrade head
    ```

6.  **Popule o Banco com Dados Mocados:**
    * Execute o script para preencher as tabelas com dados de 2015 a 2025.
    ```bash
    python scripts/populate_db.py
    ```

7.  **Inicie a Aplicação:**
    * Execute o servidor Uvicorn. A flag `--reload` reinicia o servidor a cada alteração no código.
    ```bash
    uvicorn app.main:app --reload
    ```
    A aplicação estará disponível em `http://127.0.0.1:8000`.
