from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List, Optional

from sqlalchemy import func
# from sqlalchemy.sql.functions import func
from .. import models, schemas, oauth2
from ..database import get_db

router = APIRouter(
    prefix="/objective",
    tags=['Objective']
)


@router.get("/main", response_model=List[schemas.MainObjectiveOut])
def get_main_objectives(db: Session = Depends(get_db)):

    objective = db.query(models.MainObjective).order_by(models.MainObjective.no).all()

    if not objective:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Main Objectives were not found")

    return objective

@router.get("/sub", response_model=List[schemas.SubObjectiveOut])
def get_sub_objectives(db: Session = Depends(get_db)):

    objective = db.query(models.SubObjective).all()

    if not objective:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Sub Objectives were not found")

    return objective

@router.get("/main/{id}", response_model=schemas.MainObjectiveOut)
def get_main_objective(id: int, db: Session = Depends(get_db)):

    objective = db.query(models.MainObjective).filter(models.MainObjective.id == id).first()

    if not objective:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Main Objective with id: {id} was not found")

    return objective

@router.get("/sub/{id}", response_model=schemas.SubObjectiveOut)
def get_sub_objective(id: int, db: Session = Depends(get_db)):

    objective = db.query(models.SubObjective).filter(models.SubObjective.id == id).first()

    if not objective:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Sub Objective with id: {id} was not found")

    return objective


@router.post("/main", status_code=status.HTTP_201_CREATED)
def create_main_objective(main_objective: schemas.MainObjectiveCreate, db: Session = Depends(get_db)):

    new_objective = models.MainObjective(**main_objective.model_dump())
    db.add(new_objective)
    db.commit()
    db.refresh(new_objective)

    return new_objective

@router.post("/sub", status_code=status.HTTP_201_CREATED)
def create_sub_objective(sub_objective: schemas.SubObjectiveCreate, db: Session = Depends(get_db)):

    new_objective = models.SubObjective(**sub_objective.model_dump())
    db.add(new_objective)
    db.commit()
    db.refresh(new_objective)

    return new_objective


@router.put("/main/{id}", response_model=schemas.MainObjectiveOut)
def update_main_objective(id: int, updates: schemas.MainObjectiveCreate, db: Session = Depends(get_db)):

    objective_query = db.query(models.MainObjective).filter(models.MainObjective.id == id)

    objective = objective_query.first()

    if objective == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Main Objective with id: {id} does not exist")

    objective_query.update(updates.model_dump(), synchronize_session=False)

    db.commit()

    return objective_query.first()

@router.put("/sub/{id}", response_model=schemas.SubObjectiveOut)
def update_sub_objective(id: int, updates: schemas.SubObjectiveCreate, db: Session = Depends(get_db)):

    objective_query = db.query(models.SubObjective).filter(models.SubObjective.id == id)

    objective = objective_query.first()

    if objective == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Sub Objective with id: {id} does not exist")

    objective_query.update(updates.model_dump(), synchronize_session=False)

    db.commit()

    return objective_query.first()

@router.delete("/main/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_main_objective(id: int, db: Session = Depends(get_db)):

    objective_query = db.query(models.MainObjective).filter(models.MainObjective.id == id)

    objective = objective_query.first()

    if objective == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Main Objective with id: {id} does not exist")

    objective_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.delete("/sub/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_sub_objective(id: int, db: Session = Depends(get_db)):

    objective_query = db.query(models.SubObjective).filter(models.SubObjective.id == id)

    objective = objective_query.first()

    if objective == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Sub Objective with id: {id} does not exist")

    objective_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)