from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List, Optional

from sqlalchemy import func
# from sqlalchemy.sql.functions import func
from .. import models, schemas, oauth2
from ..database import get_db

router = APIRouter(
    prefix="/tag",
    tags=['Tag']
)


@router.get("", response_model=List[schemas.TagOut])
def get_tags(db: Session = Depends(get_db)):

    tag = db.query(models.Tag).all()

    if not tag:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"tags were not found")

    return tag

@router.get("/{id}", response_model=schemas.TagOut)
def get_tag(id: int, db: Session = Depends(get_db)):

    tag = db.query(models.Tag).filter(models.Tag.id == id).first()

    if not tag:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"tag with id: {id} was not found")

    return tag


@router.post("", status_code=status.HTTP_201_CREATED)
def create_tag(tag: schemas.TagCreate, db: Session = Depends(get_db)):

    new_tag = models.Tag(**tag.model_dump())
    db.add(new_tag)
    db.commit()
    db.refresh(new_tag)

    return new_tag


@router.put("/{id}", response_model=schemas.TagOut)
def update_tag(id: int, updates: schemas.TagCreate, db: Session = Depends(get_db)):

    tag_query = db.query(models.Tag).filter(models.Tag.id == id)

    tag = tag_query.first()

    if tag == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"tag with id: {id} does not exist")

    tag_query.update(updates.model_dump(), synchronize_session=False)

    db.commit()

    return tag_query.first()


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_tag(id: int, db: Session = Depends(get_db)):

    tag_query = db.query(models.Tag).filter(models.Tag.id == id)

    tag = tag_query.first()

    if tag == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"tag with id: {id} does not exist")

    tag_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)