from fastapi import Response, status, HTTPException, Depends, APIRouter
from typing import List
from sqlalchemy import asc
from sqlalchemy.orm import Session
from .. import models, schemas
from ..database import get_db
from ..utils.fastapi_users import current_active_user

router = APIRouter(
    prefix="/objective",
    tags=['Objective']
)

@router.get("/sub", 
            response_model=List[schemas.SubObjectiveOutDetail])
def get_sub_objectives(db: Session = Depends(get_db),
                       user: models.User = Depends(current_active_user)):

    objective = (db.query(models.SubObjective)
                 .filter(models.MainObjective.municipality_id == user.municipality_id)
                 .join(models.MainObjective)
                 .order_by(asc(models.MainObjective.no),asc(models.SubObjective.no))
                 .all())

    if not objective:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Sub Objectives were not found")

    return objective


@router.get("/sub/{id}", 
            response_model=schemas.SubObjectiveOut)
def get_sub_objective(id: int, 
                      db: Session = Depends(get_db),
                      user: models.User = Depends(current_active_user)):

    objective = (db.query(models.SubObjective)
                 .filter(models.SubObjective.id == id)
                 .first())
    
    if not objective:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Sub Objective with id: {id} was not found")
    
    if not (user.is_superuser or objective.municipality_id == user.municipality_id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to get this objective")

    return objective

@router.post("/sub", 
             status_code=status.HTTP_201_CREATED, 
             response_model=schemas.SubObjectiveOutDetail)
def create_sub_objective(sub_objective: schemas.SubObjectiveCreate, 
                         db: Session = Depends(get_db),
                         user: models.User = Depends(current_active_user)):

    sub_objective_dict = sub_objective.model_dump()
    sub_objective_dict['municipality_id'] = user.municipality_id
    sub_objective_dict['created_by'] = user.id
    sub_objective_dict['last_edited_by'] = user.id

    new_objective = models.SubObjective(**sub_objective_dict)
    db.add(new_objective)
    db.commit()
    db.refresh(new_objective)

    return new_objective

@router.patch("/sub/{id}", 
            response_model=schemas.SubObjectiveOutDetail)
def update_sub_objective(id: int, 
                         updates: schemas.SubObjectiveUpdate, 
                         db: Session = Depends(get_db),
                         user: models.User = Depends(current_active_user)):

    objective_query = (db.query(models.SubObjective)
                       .filter(models.SubObjective.id == id))

    objective = objective_query.first()

    if objective == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Sub Objective with id: {id} does not exist")
    
    if not (user.is_superuser or objective.municipality_id == user.municipality_id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to update this objective")
    
    updates_dict = updates.model_dump(exclude_unset=True)
    updates_dict['last_edited_by'] = user.id

    objective_query.update(updates_dict, synchronize_session=False)

    db.commit()

    return objective_query.first()


@router.delete("/sub/{id}", 
               status_code=status.HTTP_204_NO_CONTENT)
def delete_sub_objective(id: int, 
                         db: Session = Depends(get_db),
                         user: models.User = Depends(current_active_user)):

    objective_query = (db.query(models.SubObjective)
                       .filter(models.SubObjective.id == id))

    objective = objective_query.first()

    if objective == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Sub Objective with id: {id} does not exist")
    
    if not (user.is_superuser or objective.municipality_id == user.municipality_id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to delete this objective")

    objective_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)