from fastapi import FastAPI
from app.api.v1.api import api_router
from fastapi_pagination import add_pagination

app = FastAPI(
    title="FinTrackerAPI",
    version="0.1.0",
    description="Uma API para rastreamento financeiro pessoal.",
    contact={
        "name": "Stricter",
        "url": "https://github.com/StricterBot/fintracker_api",
        "email": "stricterbot@gmail.com",
    },
    license_info={
        "name": "MIT",
        "url": "https://opensource.org/licenses/MIT",
    },
)

# Inclui todas as rotas da v1 sob o prefixo /api/v1
app.include_router(api_router, prefix="/api/v1")

# Adiciona o middleware de paginação à aplicação
add_pagination(app)

@app.get("/", tags=["Root"], include_in_schema=False)
def read_root():
    return {"message": "Bem-vindo à FinTrackerAPI"}

@app.get("/health", tags=["Health"], summary="Verifica a saúde da aplicação")
def health_check():
    """Verifica se a aplicação está online e respondendo."""
    return {"status": "ok"}
