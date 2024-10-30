from typing import List
from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import models, schemas
from ..database import get_db
from ..utils.fastapi_users import current_active_user

router = APIRouter(
    prefix="/text-block",
    tags=['Text Block']
)

@router.get("", 
            response_model=List[schemas.TextBlockOut])
def get_text_blocks(db: Session = Depends(get_db),
                    user: models.User = Depends(current_active_user)):

    text_blocks = (db.query(models.TextBlock)
                   .filter(models.TextBlock.municipality_id == user.municipality_id)
                   .order_by(models.TextBlock.label).all())

    if not text_blocks:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"text blocks were not found")

    return text_blocks

@router.get("/{id}", 
            response_model=schemas.TextBlockOut)
def get_text_block(id: int,
                   db: Session = Depends(get_db),
                   user: models.User = Depends(current_active_user)):

    text_block = (db.query(models.TextBlock)
                  .filter(models.TextBlock.id == id)
                  .first())
    
    if not text_block:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"text block with id: {id} was not found")
    
    if not (user.is_superuser or text_block.municipality_id == user.municipality_id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to get this text block")

    return text_block


@router.post("", 
             status_code=status.HTTP_201_CREATED, 
             response_model=schemas.TextBlockOut)
def create_text_block(text_block: schemas.TextBlockCreate, 
                      db: Session = Depends(get_db),
                      user: models.User = Depends(current_active_user)):

    new_text_block = models.TextBlock(label=text_block.label,
                                      municipality_id=user.municipality_id,
                                      created_by=user.id,
                                      last_edited_by=user.id)
    
    db.add(new_text_block)
    db.commit()
    db.refresh(new_text_block)

    # Add associations with indicators
    if text_block.tag_ids:
        tags = (db.query(models.Tag)
                .filter(models.Tag.id.in_(text_block.tag_ids))
                .all())
        new_text_block.tags.extend(tags)
    
    db.commit()
    db.refresh(new_text_block)

    return new_text_block

@router.patch("/{id}", 
            response_model=schemas.TextBlockOut)
def update_text_block(id: int, 
                      updates: schemas.TextBlockUpdate, 
                      db: Session = Depends(get_db),
                      user: models.User = Depends(current_active_user)):

    text_block_query = (db.query(models.TextBlock)
                        .filter(models.TextBlock.id == id))

    text_block = text_block_query.first()

    if not text_block:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"text block with id: {id} does not exist")
    
    if not (user.is_superuser or text_block.municipality_id == user.municipality_id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to update this text block")
    
    # Update main fields, excluding indicator_ids
    update_data = updates.model_dump(exclude_unset=True, exclude={'tag_ids'})
    update_data['last_edited_by'] = user.id
    for field, value in update_data.items():
        setattr(text_block, field, value)

    # Update indicators association only if indicator_ids is provided
    if updates.tag_ids is not None:
        # Clear existing associations with indicators
        text_block.tags.clear()

        tags = db.query(models.Tag).filter(models.Tag.id.in_(updates.tag_ids)).all()
        text_block.tags = tags
    
    db.commit()
    db.refresh(text_block)

    return text_block

@router.delete("/{id}", 
               status_code=status.HTTP_204_NO_CONTENT)
def delete_text_block(id: int, 
                      db: Session = Depends(get_db),
                      user: models.User = Depends(current_active_user)):

    text_block_query = (db.query(models.TextBlock)
                        .filter(models.TextBlock.id == id))

    text_block = text_block_query.first()

    if text_block == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"text block with id: {id} does not exist")
    
    if not (user.is_superuser or text_block.municipality_id == user.municipality_id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to delete this text block")

    text_block_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)