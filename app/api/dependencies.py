from sqlalchemy.orm import Session
from app.database.session import SessionLocal

def get_db():
    """
    Função de dependência que cria e gerencia uma sessão de banco de dados por requisição.
    Garante que a sessão seja sempre fechada após o uso.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()