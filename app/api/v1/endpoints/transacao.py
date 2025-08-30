from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import select, or_
from typing import Optional

from fastapi_pagination import Page
from fastapi_pagination.ext.sqlalchemy import paginate as sqlalchemy_paginate

from app import models, schemas
from app.api.dependencies import get_db

router = APIRouter()

@router.post("/", response_model=schemas.TransacaoRead)
async def realizar_transacao(transacao: schemas.TransacaoCreate, db: Session = Depends(get_db)):

    try:
        if transacao.carteira_origem_id == transacao.carteira_destino_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="A carteira de origem e destino não podem ser a mesma."
            )

        stmt_origem = select(models.Carteira).where(models.Carteira.id == transacao.carteira_origem_id)
        carteira_origem = db.execute(stmt_origem).scalar_one_or_none()

        stmt_destino = select(models.Carteira).where(models.Carteira.id == transacao.carteira_destino_id)
        carteira_destino = db.execute(stmt_destino).scalar_one_or_none()

        if not carteira_origem or not carteira_destino:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Uma ou ambas as carteiras não foram encontradas."
            )
        
        if carteira_origem.moeda != carteira_destino.moeda:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Transferências só são permitidas entre carteiras da mesma moeda."
            )

        if carteira_origem.saldo_atual < transacao.valor:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Saldo insuficiente na carteira de origem."
            )
            
        carteira_origem.saldo_atual -= transacao.valor
        carteira_destino.saldo_atual += transacao.valor

        db_transacao = models.Transacao(
            valor=transacao.valor,
            carteira_origem_id=transacao.carteira_origem_id,
            carteira_destino_id=transacao.carteira_destino_id
        )
        db.add(db_transacao)
        
        db.commit()
        db.refresh(db_transacao)
        
        return db_transacao

    except HTTPException:
        db.rollback()
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ocorreu um erro inesperado na transação: {e}"
        )

@router.get("/", response_model=Page[schemas.TransacaoRead])
async def listar_transacoes(
    db: Session = Depends(get_db),
    carteira_id: Optional[int] = None # Filtro opcional
):
    query = select(models.Transacao).order_by(models.Transacao.timestamp.desc())

    if carteira_id:
        query = query.where(
            or_(
                models.Transacao.carteira_origem_id == carteira_id,
                models.Transacao.carteira_destino_id == carteira_id
            )
        )
        
    return sqlalchemy_paginate(db, query)