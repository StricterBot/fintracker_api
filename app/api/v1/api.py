from fastapi import APIRouter
from app.api.v1.endpoints import usuario, cartao, carteira, transacao

api_router = APIRouter()

api_router.include_router(usuario.router, prefix="/usuarios", tags=["Usuarios"])
api_router.include_router(carteira.router, prefix="/carteiras", tags=["Carteiras"])
api_router.include_router(cartao.router, prefix="/cartoes", tags=["Cartoes"])
api_router.include_router(transacao.router, prefix="/transacoes", tags=["Transações"])