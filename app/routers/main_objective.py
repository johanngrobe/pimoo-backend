from typing import List
from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import models, schemas
from ..database import get_db
from ..utils.fastapi_users import current_active_user

router = APIRouter(
    prefix="/objective",
    tags=['Objective']
)

@router.get("/main", 
            response_model=List[schemas.MainObjectiveOut])
def get_main_objectives(db: Session = Depends(get_db),
                        user: models.User = Depends(current_active_user)):

    objective = (db.query(models.MainObjective)
                 .filter(models.MainObjective.municipality_id == user.municipality_id)
                 .order_by(models.MainObjective.no).all())

    if not objective:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Main Objectives were not found")

    return objective

@router.get("/main/{id}", 
            response_model=schemas.MainObjectiveOut)
def get_main_objective(id: int, 
                       db: Session = Depends(get_db),
                       user: models.User = Depends(current_active_user)):

    objective = db.query(models.MainObjective).filter(models.MainObjective.id == id).first()

    if not objective:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Main Objective with id: {id} was not found")
    
    if not (user.is_superuser or objective.municipality_id == user.municipality_id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to get this objective")

    return objective

@router.post("/main", 
             status_code=status.HTTP_201_CREATED)
def create_main_objective(main_objective: schemas.MainObjectiveCreate, 
                          db: Session = Depends(get_db),
                          user: models.User = Depends(current_active_user)):
    
    main_objective_dict = main_objective.model_dump()
    main_objective_dict['municipality_id'] = user.municipality_id
    main_objective_dict['created_by'] = user.id
    main_objective_dict['last_edited_by'] = user.id

    new_objective = models.MainObjective(**main_objective_dict)
    db.add(new_objective)
    db.commit()
    db.refresh(new_objective)

    return new_objective

@router.patch("/main/{id}", 
            response_model=schemas.MainObjectiveOut)
def update_main_objective(id: int, 
                          updates: schemas.MainObjectiveUpdate, 
                          db: Session = Depends(get_db),
                          user: models.User = Depends(current_active_user)):

    objective_query = (db.query(models.MainObjective)
                       .filter(models.MainObjective.id == id))

    objective = objective_query.first()

    if objective == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Main Objective with id: {id} does not exist")
    
    if not (user.is_superuser or objective.municipality_id == user.municipality_id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to update this objective")
    
    objective_dict = updates.model_dump(exclude_unset=True)
    objective_dict['last_edited_by'] = user.id

    objective_query.update(objective_dict, synchronize_session=False)

    db.commit()

    return objective_query.first()

@router.delete("/main/{id}", 
               status_code=status.HTTP_204_NO_CONTENT)
def delete_main_objective(id: int, 
                          db: Session = Depends(get_db),
                          user: models.User = Depends(current_active_user)):

    objective_query = (db.query(models.MainObjective)
                       .filter(models.MainObjective.id == id))

    objective = objective_query.first()

    if objective == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Main Objective with id: {id} does not exist")
    
    if not (user.is_superuser or objective.municipality_id == user.municipality_id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to delete this objective")

    objective_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)