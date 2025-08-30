from sqlalchemy import Column, Integer, String, Numeric, ForeignKey
from sqlalchemy.orm import relationship

from app.database.base import Base

class Carteira(Base):
    __tablename__ = "carteiras"

    id = Column(Integer, primary_key=True, index=True)
    saldo_atual = Column(Numeric(10, 2), nullable=False, default=0.00)
    moeda = Column(String(3), nullable=False, default="BRL") # Ex: BRL, USD

    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    usuario = relationship("Usuario", back_populates="carteiras")  
    cartoes = relationship("Cartao", back_populates="carteira", cascade="all, delete-orphan")

    transacoes_enviadas = relationship(
        "Transacao",
        foreign_keys="[Transacao.carteira_origem_id]",
        back_populates="carteira_origem"
    )
    transacoes_recebidas = relationship(
        "Transacao",
        foreign_keys="[Transacao.carteira_destino_id]",
        back_populates="carteira_destino"
    )