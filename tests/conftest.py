import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.database.base import Base
from app.api.dependencies import get_db

# Usa um banco de dados SQLite em memória para os testes
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    """Sobrescreve a dependência get_db para usar o banco de dados de teste."""
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

# Aplica a sobrescrita da dependência na aplicação
app.dependency_overrides[get_db] = override_get_db

@pytest.fixture(scope="function")
def client():
    """
    Fixture que gerencia o ciclo de vida do banco de dados e fornece um TestClient.
    - Cria todas as tabelas antes de cada teste.
    - Fornece um cliente para fazer as requisições.
    - Limpa (dropa) todas as tabelas depois de cada teste.
    Isso garante 100% de isolamento entre os testes.
    """
    Base.metadata.create_all(bind=engine)
    with TestClient(app) as c:
        yield c
    Base.metadata.drop_all(bind=engine)