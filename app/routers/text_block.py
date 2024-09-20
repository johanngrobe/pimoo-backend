from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List, Optional

from sqlalchemy import func
# from sqlalchemy.sql.functions import func
from .. import models, schemas, oauth2
from ..database import get_db

router = APIRouter(
    prefix="/text-block",
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


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.TextBlockOut)
def create_text_block(text_block: schemas.TextBlockCreate, db: Session = Depends(get_db)):

    new_text_block = models.TextBlock(
        label=text_block.label
    )
    
    db.add(new_text_block)
    db.commit()
    db.refresh(new_text_block)

    # Add associations with indicators
    if text_block.tag_ids:
        tags = db.query(models.Tag).filter(models.Tag.id.in_(text_block.tag_ids)).all()
        new_text_block.tags.extend(tags)
    
    db.commit()
    db.refresh(new_text_block)

    return new_text_block


@router.put("/{id}", response_model=schemas.TextBlockOut)
def update_text_block(id: int, updates: schemas.TextBlockCreate, db: Session = Depends(get_db)):

    text_block_query = db.query(models.TextBlock).filter(models.TextBlock.id == id)

    text_block = text_block_query.first()

    text_block.label = updates.label
    
    # Clear existing associations with indicators
    text_block.tags.clear()

    # Add new indicators
    if updates.tag_ids:
        tags = db.query(models.Tag).filter(models.Tag.id.in_(updates.tag_ids)).all()
        text_block.tags = tags
    
    db.commit()
    db.refresh(text_block)

    return text_block

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