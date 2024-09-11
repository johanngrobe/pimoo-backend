from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List, Optional

from sqlalchemy import func
# from sqlalchemy.sql.functions import func
from .. import models, schemas, oauth2
from ..database import get_db

router = APIRouter(
    prefix="/text_block",
    tags=['Text Block']
)


@router.get("/", response_model=List[schemas.TextBlockOut])
def get_text_blocks(db: Session = Depends(get_db)):

    text_blocks = db.query(models.TextBlock).order_by(models.TextBlock.label).all()

    if not text_blocks:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"text blocks were not found")

    return text_blocks

@router.get("/{id}", response_model=schemas.TextBlockOut)
def get_text_block(id: int, db: Session = Depends(get_db)):

    text_block = db.query(models.TextBlock).filter(models.TextBlock.id == id).first()

    if not text_block:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"text block with id: {id} was not found")

    return text_block


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_text_block(text_block: schemas.TextBlockCreate, db: Session = Depends(get_db)):

    new_text_block = models.TextBlock(**text_block.model_dump())
    db.add(new_text_block)
    db.commit()
    db.refresh(new_text_block)

    return new_text_block


@router.put("/{id}", response_model=schemas.TextBlockOut)
def update_text_block(id: int, updates: schemas.TextBlockCreate, db: Session = Depends(get_db)):

    text_block_query = db.query(models.TextBlock).filter(models.TextBlock.id == id)

    text_block = text_block_query.first()

    if text_block == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"text block with id: {id} does not exist")

    # if post.owner_id != current_user.id:
    #     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
    #                         detail="Not authorized to perform requested action")

    text_block_query.update(updates.model_dump(), synchronize_session=False)

    db.commit()

    return text_block_query.first()

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_text_block(id: int, db: Session = Depends(get_db)):

    text_block_query = db.query(models.TextBlock).filter(models.TextBlock.id == id)

    text_block = text_block_query.first()

    if text_block == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"text block with id: {id} does not exist")

    text_block_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)