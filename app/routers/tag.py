from typing import List
from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import models, schemas
from ..database import get_db
from ..utils.fastapi_users import current_active_user

router = APIRouter(
    prefix="/tag",
    tags=['Tag']
)

@router.get("", 
            response_model=List[schemas.TagOut])
def get_tags(db: Session = Depends(get_db),
             user: models.User = Depends(current_active_user)):

    tags = (db.query(models.Tag)
           .filter(models.Tag.municipality_id == user.municipality_id)
           .all())

    if not tags:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"tags were not found")

    return tags

@router.get("/{id}", 
            response_model=schemas.TagOut)
def get_tag(id: int,
            db: Session = Depends(get_db),
            user: models.User = Depends(current_active_user)):

    tag = (db.query(models.Tag)
           .filter(models.Tag.id == id)
           .first())

    if not tag:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"tag with id: {id} was not found")
    
    if not (user.is_superuser or tag.municipality_id == user.municipality_id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to get this tag")

    return tag


@router.post("", 
             status_code=status.HTTP_201_CREATED)
def create_tag(tag: schemas.TagCreate, 
               db: Session = Depends(get_db),
               user: models.User = Depends(current_active_user)):
    
    tag_dict = tag.model_dump()
    tag_dict['municipality_id'] = user.municipality_id
    tag_dict['created_by'] = user.id
    tag_dict['last_edited_by'] = user.id

    new_tag = models.Tag(**tag_dict)
    db.add(new_tag)
    db.commit()
    db.refresh(new_tag)

    return new_tag


@router.patch("/{id}", 
            response_model=schemas.TagOut)
def update_tag(id: int, 
               updates: schemas.TagUpdate, 
               db: Session = Depends(get_db),
               user: models.User = Depends(current_active_user)):

    tag_query = (db.query(models.Tag)
                 .filter(models.Tag.id == id))

    tag = tag_query.first()

    if tag == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"tag with id: {id} does not exist")
    
    if not (user.is_superuser or tag.municipality_id == user.municipality_id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to update this tag")
    
    updates_dict = updates.model_dump(exclude_unset=True)
    updates_dict['last_edited_by'] = user.id

    tag_query.update(updates_dict, synchronize_session=False)

    db.commit()

    return tag_query.first()


@router.delete("/{id}", 
               status_code=status.HTTP_204_NO_CONTENT)
def delete_tag(id: int, 
               db: Session = Depends(get_db),
               user: models.User = Depends(current_active_user)):

    tag_query = db.query(models.Tag).filter(models.Tag.id == id)

    tag = tag_query.first()

    if tag == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"tag with id: {id} does not exist")
    
    if not (user.is_superuser or tag.municipality_id == user.municipality_id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to delete this tag")

    tag_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)