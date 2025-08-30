from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select

from fastapi_pagination import Page
from fastapi_pagination.ext.sqlalchemy import paginate as sqlalchemy_paginate

from app import models, schemas
from app.api.dependencies import get_db

router = APIRouter()

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UsuarioRead)
async def create_usuario(usuario: schemas.UsuarioCreate, db: Session = Depends(get_db)):
    """ Cria um novo usuário no banco de dados. """
    db_usuario = models.Usuario(**usuario.model_dump())
    db.add(db_usuario)
    try:
        db.commit()
        db.refresh(db_usuario)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="CPF ou Email já cadastrado no sistema."
        )
    return db_usuario

@router.get("/", response_model=Page[schemas.UsuarioRead])
async def read_usuarios(db: Session = Depends(get_db)):
    """ Retorna uma lista paginada de todos os usuários. """
    return sqlalchemy_paginate(db, select(models.Usuario))

@router.get("/{usuario_id}", response_model=schemas.UsuarioRead)
async def read_usuario(usuario_id: int, db: Session = Depends(get_db)):
    """ Retorna os dados de um usuário específico, buscando pelo seu ID. """
    statement = select(models.Usuario).where(models.Usuario.id == usuario_id)
    db_usuario = db.execute(statement).scalar_one_or_none()
    
    if db_usuario is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuário não encontrado")
    return db_usuario

@router.put("/{usuario_id}", response_model=schemas.UsuarioRead)
async def update_usuario(usuario_id: int, usuario: schemas.UsuarioUpdate, db: Session = Depends(get_db)):
    """ Atualiza as informações de um usuário existente. """
    statement = select(models.Usuario).where(models.Usuario.id == usuario_id)
    db_usuario = db.execute(statement).scalar_one_or_none()

    if db_usuario is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuário não encontrado")

    update_data = usuario.model_dump(exclude_unset=True)
    
    for key, value in update_data.items():
        setattr(db_usuario, key, value)

    db.add(db_usuario)
    db.commit()
    db.refresh(db_usuario)
    return db_usuario

@router.delete("/{usuario_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_usuario(usuario_id: int, db: Session = Depends(get_db)):
    """ Deleta um usuário do banco de dados. """
    statement = select(models.Usuario).where(models.Usuario.id == usuario_id)
    db_usuario = db.execute(statement).scalar_one_or_none()

    if db_usuario is None:
        # É uma boa prática não vazar se o usuário existia ou não no delete
        # Mas para consistência com o resto do CRUD, vamos manter o 404
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuário não encontrado")

    db.delete(db_usuario)
    db.commit()
    return None