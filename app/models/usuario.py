from sqlalchemy import Column, Integer, String, DateTime, func
from sqlalchemy.orm import relationship

from app.database.base import Base

class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(100), nullable=False)
    cpf = Column(String(11), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    data_criacao = Column(DateTime, server_default=func.now())

    # Relacionamento: Um usuário pode ter várias carteiras
    carteiras = relationship("Carteira", back_populates="usuario", cascade="all, delete-orphan")