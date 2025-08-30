from pydantic import BaseModel, Field, ConfigDict
from decimal import Decimal
from datetime import datetime

class TransacaoCreate(BaseModel):
    carteira_origem_id: int
    carteira_destino_id: int
    valor: Decimal = Field(gt=0, description="O valor a ser transferido")

class TransacaoRead(BaseModel):
    """ Schema para representar um registro de transação lido do banco. """
    id: int
    valor: Decimal
    timestamp: datetime
    carteira_origem_id: int
    carteira_destino_id: int

    model_config = ConfigDict(from_attributes=True)