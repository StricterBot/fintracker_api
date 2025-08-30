from pydantic import BaseModel, EmailStr, ConfigDict
from datetime import datetime
from typing import Optional, List

class CarteiraReadSimple(BaseModel):
    id: int
    moeda: str
    saldo_atual: float

    model_config = ConfigDict(from_attributes=True)


class UsuarioBase(BaseModel):
    nome: str
    email: EmailStr
    cpf: str

class UsuarioCreate(UsuarioBase):
    pass

class UsuarioUpdate(BaseModel):
    nome: Optional[str] = None
    email: Optional[EmailStr] = None

class UsuarioRead(UsuarioBase):
    id: int
    data_criacao: datetime
    carteiras: List[CarteiraReadSimple] = []

    model_config = ConfigDict(from_attributes=True)