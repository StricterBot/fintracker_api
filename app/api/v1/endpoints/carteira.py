from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Optional
from fastapi_pagination import Page
from fastapi_pagination.ext.sqlalchemy import paginate as sqlalchemy_paginate

from sqlalchemy import select

from app import models, schemas
from app.api.dependencies import get_db

router = APIRouter()

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.CarteiraRead)
async def create_carteira(carteira: schemas.CarteiraCreate, db: Session = Depends(get_db)):
    """
    Cria uma nova carteira para um usuário.
    - Aprimoramento: Verifica se o usuário (dono da carteira) existe antes de criar.
    """
    statement = select(models.Usuario).where(models.Usuario.id == carteira.usuario_id)
    db_usuario = db.execute(statement).scalar_one_or_none()

    if not db_usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Usuário com id {carteira.usuario_id} não encontrado."
        )
    
    db_carteira = models.Carteira(**carteira.model_dump())
    db.add(db_carteira)
    db.commit()
    db.refresh(db_carteira)
    return db_carteira

@router.get("/", response_model=Page[schemas.CarteiraRead])
async def read_carteiras(db: Session = Depends(get_db), usuario_id: Optional[int] = None):
    """
    Retorna uma lista paginada de carteiras.
    - Aprimoramento: Permite filtrar as carteiras por `usuario_id` via query parameter.
    """
    query = select(models.Carteira)
    if usuario_id:
        query = query.where(models.Carteira.usuario_id == usuario_id)
    
    return sqlalchemy_paginate(db, query)

@router.get("/{carteira_id}", response_model=schemas.CarteiraRead)
async def read_carteira(carteira_id: int, db: Session = Depends(get_db)):
    """
    Retorna os dados de uma carteira específica pelo seu ID.
    """
    statement = select(models.Carteira).where(models.Carteira.id == carteira_id)
    db_carteira = db.execute(statement).scalar_one_or_none()

    if db_carteira is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Carteira não encontrada")
    return db_carteira

@router.put("/{carteira_id}", response_model=schemas.CarteiraRead)
async def update_carteira(carteira_id: int, carteira: schemas.CarteiraUpdate, db: Session = Depends(get_db)):
    """
    Atualiza informações de uma carteira.
    """
    statement = select(models.Carteira).where(models.Carteira.id == carteira_id)
    db_carteira = db.execute(statement).scalar_one_or_none()

    if db_carteira is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Carteira não encontrada")

    update_data = carteira.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_carteira, key, value)

    db.add(db_carteira)
    db.commit()
    db.refresh(db_carteira)
    return db_carteira

@router.delete("/{carteira_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_carteira(carteira_id: int, db: Session = Depends(get_db)):
    """
    Deleta uma carteira.
    """
    statement = select(models.Carteira).where(models.Carteira.id == carteira_id)
    db_carteira = db.execute(statement).scalar_one_or_none()

    if db_carteira:
        db.delete(db_carteira)
        db.commit()
    return None