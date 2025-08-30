from sqlalchemy import Column, Integer, String, Numeric, ForeignKey
from sqlalchemy.orm import relationship

from app.database.base import Base

class Cartao(Base):
    __tablename__ = "cartoes"

    id = Column(Integer, primary_key=True, index=True)
    numero = Column(String(16), unique=True, nullable=False)
    validade = Column(String(5), nullable=False) # Formato "MM/YY"
    limite = Column(Numeric(10, 2), nullable=False)

    # Chave Estrangeira para a carteira
    carteira_id = Column(Integer, ForeignKey("carteiras.id"), nullable=False)

    # Relacionamento de volta para a carteira
    carteira = relationship("Carteira", back_populates="cartoes")