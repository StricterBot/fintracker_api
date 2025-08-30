from pydantic import BaseModel, ConfigDict
from typing import Optional, List
from decimal import Decimal

class CartaoReadSimple(BaseModel):
    id: int
    numero: str

    model_config = ConfigDict(from_attributes=True)


class CarteiraBase(BaseModel):
    moeda: str = "BRL"
    saldo_atual: Decimal

class CarteiraCreate(CarteiraBase):
    usuario_id: int

class CarteiraUpdate(BaseModel):
    saldo_atual: Optional[Decimal] = None

class CarteiraRead(CarteiraBase):
    id: int
    usuario_id: int
    cartoes: List[CartaoReadSimple] = []

    model_config = ConfigDict(from_attributes=True)