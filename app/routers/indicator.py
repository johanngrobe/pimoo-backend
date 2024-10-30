from typing import List
from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import models, schemas
from ..database import get_db
from ..utils.fastapi_users import current_active_user

router = APIRouter(
    prefix="/indicator",
    tags=['Indicator']
)

@router.get("", 
            response_model=List[schemas.IndicatorOut])
def get_indicators(db: Session = Depends(get_db),
                   user: models.User = Depends(current_active_user)):

    indicators = (db.query(models.Indicator)
                  .filter(models.Indicator.municipality_id == user.municipality_id)
                  .order_by(models.Indicator.label).all())

    if not indicators:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"indicators were not found")

    return indicators

@router.get("/{id}", 
            response_model=schemas.IndicatorOut)
def get_indicator(id: int, 
                  db: Session = Depends(get_db),
                  user: models.User = Depends(current_active_user)):

    indicator = (db.query(models.Indicator)
                 .filter(models.Indicator.id == id)
                 .first())

    if not indicator:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"indicator with id: {id} was not found")
    
    if not (user.is_superuser or indicator.municipality_id == user.municipality_id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to get this indicator")

    return indicator


@router.post("", 
             status_code=status.HTTP_201_CREATED, 
             response_model=schemas.IndicatorOut)
def create_indicator(indicator: schemas.IndicatorCreate, 
                     db: Session = Depends(get_db),
                     user: models.User = Depends(current_active_user)):

    new_indicator = models.Indicator(label=indicator.label,
                                     source_url=indicator.source_url,
                                     municipality_id=user.municipality_id,
                                     created_by=user.id,
                                     last_edited_by=user.id)
    
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


@router.patch("/{id}", 
            response_model=schemas.IndicatorOut)
def update_indicator(id: int, 
                     updates: schemas.IndicatorUpdate, 
                     db: Session = Depends(get_db),
                     user: models.User = Depends(current_active_user)):

    indicator_query = (db.query(models.Indicator)
                       .filter(models.Indicator.id == id))
    
    indicator = indicator_query.first()

    if not (user.is_superuser or indicator.municipality_id == user.municipality_id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to update this indicator")
    
    updates_dict = updates.model_dump(exclude_unset=True, exclude={'tag_ids'})
    updates_dict['last_edited_by'] = user.id

    for key, value in updates_dict.items():
        setattr(indicator, key, value)
    
    # Add new indicators
    if updates.tag_ids is not None:
        # Clear existing associations with indicators
        indicator.tags.clear()

        tags = db.query(models.Tag).filter(models.Tag.id.in_(updates.tag_ids)).all()
        indicator.tags = tags
    
    db.commit()
    db.refresh(indicator)

    return indicator

@router.delete("/{id}", 
               status_code=status.HTTP_204_NO_CONTENT)
def delete_indicator(id: int, 
                     db: Session = Depends(get_db),
                     user: models.User = Depends(current_active_user)):

    indicator_query = db.query(models.Indicator).filter(models.Indicator.id == id)

    indicator = indicator_query.first()

    if indicator == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"indicator with id: {id} does not exist")
    
    if not (user.is_superuser or indicator.municipality_id == user.municipality_id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to delete this indicator")

    indicator_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)