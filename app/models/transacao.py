from sqlalchemy import Column, Integer, Numeric, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship

from app.database.base import Base

class Transacao(Base):
    __tablename__ = "transacoes"

    id = Column(Integer, primary_key=True, index=True)
    valor = Column(Numeric(10, 2), nullable=False)
    timestamp = Column(DateTime, server_default=func.now())
    
    carteira_origem_id = Column(Integer, ForeignKey("carteiras.id"), nullable=False)
    carteira_destino_id = Column(Integer, ForeignKey("carteiras.id"), nullable=False)

    carteira_origem = relationship("Carteira", foreign_keys=[carteira_origem_id])
    carteira_destino = relationship("Carteira", foreign_keys=[carteira_destino_id])