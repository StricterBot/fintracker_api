from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Optional
from fastapi_pagination import Page
from fastapi_pagination.ext.sqlalchemy import paginate as sqlalchemy_paginate

from sqlalchemy import select

from app import models, schemas
from app.api.dependencies import get_db

router = APIRouter()

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.CartaoRead)
async def create_cartao(cartao: schemas.CartaoCreate, db: Session = Depends(get_db)):
    """
    Cria um novo cartão para uma carteira.
    - Aprimoramento: Verifica se a carteira (dona do cartão) existe antes de criar.
    """
    statement = select(models.Carteira).where(models.Carteira.id == cartao.carteira_id)
    db_carteira = db.execute(statement).scalar_one_or_none()

    if not db_carteira:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Carteira com id {cartao.carteira_id} não encontrada."
        )

    db_cartao = models.Cartao(**cartao.model_dump())
    db.add(db_cartao)
    db.commit()
    db.refresh(db_cartao)
    return db_cartao

@router.get("/", response_model=Page[schemas.CartaoRead])
async def read_cartoes(db: Session = Depends(get_db), carteira_id: Optional[int] = None):
    """
    Retorna uma lista paginada de cartões.
    - Aprimoramento: Permite filtrar os cartões por `carteira_id` via query parameter.
    """
    query = select(models.Cartao)
    if carteira_id:
        query = query.where(models.Cartao.carteira_id == carteira_id)
    
    return sqlalchemy_paginate(db, query)

@router.get("/{cartao_id}", response_model=schemas.CartaoRead)
async def read_cartao(cartao_id: int, db: Session = Depends(get_db)):
    """
    Retorna os dados de um cartão específico pelo seu ID.
    """
    statement = select(models.Cartao).where(models.Cartao.id == cartao_id)
    db_cartao = db.execute(statement).scalar_one_or_none()

    if db_cartao is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cartão não encontrado")
    return db_cartao

@router.put("/{cartao_id}", response_model=schemas.CartaoRead)
async def update_cartao(cartao_id: int, cartao: schemas.CartaoUpdate, db: Session = Depends(get_db)):
    """
    Atualiza informações de um cartão.
    """
    statement = select(models.Cartao).where(models.Cartao.id == cartao_id)
    db_cartao = db.execute(statement).scalar_one_or_none()

    if db_cartao is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cartão não encontrado")

    update_data = cartao.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_cartao, key, value)

    db.add(db_cartao)
    db.commit()
    db.refresh(db_cartao)
    return db_cartao

@router.delete("/{cartao_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_cartao(cartao_id: int, db: Session = Depends(get_db)):
    """
    Deleta um cartão.
    """
    statement = select(models.Cartao).where(models.Cartao.id == cartao_id)
    db_cartao = db.execute(statement).scalar_one_or_none()

    if db_cartao:
        db.delete(db_cartao)
        db.commit()
    return None