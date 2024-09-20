from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List, Optional

from sqlalchemy import func
# from sqlalchemy.sql.functions import func
from .. import models, schemas, oauth2
from ..database import get_db

router = APIRouter(
    prefix="/indicator",
    tags=['Indicator']
)


@router.get("/", response_model=List[schemas.IndicatorOut])
def get_indicators(db: Session = Depends(get_db)):

    indicators = db.query(models.Indicator).order_by(models.Indicator.label).all()

    if not indicators:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"indicators were not found")

    return indicators

@router.get("/{id}", response_model=schemas.IndicatorOut)
def get_indicator(id: int, db: Session = Depends(get_db)):

    indicator = db.query(models.Indicator).filter(models.Indicator.id == id).first()

    if not indicator:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"indicator with id: {id} was not found")

    return indicator


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.IndicatorOut)
def create_indicator(indicator: schemas.IndicatorCreate, db: Session = Depends(get_db)):

    new_indicator = models.TextBlock(
        label=indicator.label
    )
    
    db.add(new_indicator)
    db.commit()
    db.refresh(new_indicator)

    # Add associations with indicators
    if indicator.tag_ids:
        tags = db.query(models.Tag).filter(models.Tag.id.in_(indicator.tag_ids)).all()
        new_indicator.tags.extend(tags)
    
    db.commit()
    db.refresh(new_indicator)

    return new_indicator


@router.put("/{id}", response_model=schemas.IndicatorOut)
def update_indicator(id: int, updates: schemas.IndicatorCreate, db: Session = Depends(get_db)):

    indicator_query = db.query(models.Indicator).filter(models.Indicator.id == id)

    indicator = indicator_query.first()

    indicator.label = updates.label
    
    # Clear existing associations with indicators
    indicator.tags.clear()

    # Add new indicators
    if updates.tag_ids:
        tags = db.query(models.Tag).filter(models.Tag.id.in_(updates.tag_ids)).all()
        indicator.tags = tags
    
    db.commit()
    db.refresh(indicator)

    return indicator

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_indicator(id: int, db: Session = Depends(get_db)):

    indicator_query = db.query(models.Indicator).filter(models.Indicator.id == id)

    indicator = indicator_query.first()

    if indicator == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"indicator with id: {id} does not exist")

    indicator_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)