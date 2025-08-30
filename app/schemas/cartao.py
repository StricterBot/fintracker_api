from pydantic import BaseModel, ConfigDict, Field
from typing import Optional, Annotated
from decimal import Decimal


class CartaoBase(BaseModel):
    validade: Annotated[
        str, Field(pattern=r"^(0[1-9]|1[0-2])\/\d{2}$")
    ]
    numero: Annotated[
        str, Field(min_length=16, max_length=16)
    ]
    limite: Decimal

class CartaoCreate(CartaoBase):
    carteira_id: int

class CartaoUpdate(BaseModel):
    # Geralmente, só o limite de um cartão é atualizável
    limite: Optional[Decimal] = None

class CartaoRead(CartaoBase):
    id: int
    carteira_id: int

    model_config = ConfigDict(from_attributes=True)