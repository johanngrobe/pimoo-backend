from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List, Optional

from sqlalchemy import func
# from sqlalchemy.sql.functions import func
from .. import models, schemas, oauth2
from ..database import get_db

router = APIRouter(
    prefix="/mobility-result",
    tags=['Mobility Result']
)


@router.get("", response_model=List[schemas.MobilityResultOut])
def get_mobility_results(db: Session = Depends(get_db)):

    result = db.query(models.MobilityResult).filter(models.MobilityResult.id == id).all()

    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"indicator were not found")

    return result

@router.get("/{id}", response_model=schemas.MobilityResultOut)
def get_mobility_result(id: int, db: Session = Depends(get_db)):

    result = db.query(models.MobilityResult).filter(models.MobilityResult.id == id).first()

    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"result with id: {id} was not found")

    return result


@router.post("", status_code=status.HTTP_201_CREATED)
def create_mobility_result(mobility_result: schemas.MobilityResultCreate, db: Session = Depends(get_db)):

    new_result = models.MobilityResult(**mobility_result.model_dump())
    db.add(new_result)
    db.commit()
    db.refresh(new_result)

    return new_result


@router.put("/{id}", response_model=schemas.MobilityResultOut)
def update_mobility_result(id: int, updates: schemas.MobilityResultCreate, db: Session = Depends(get_db)):

    result_query = db.query(models.MobilityResult).filter(models.MobilityResult.id == id)

    result = result_query.first()

    if result == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"result with id: {id} does not exist")

    result_query.update(updates.model_dump(), synchronize_session=False)

    db.commit()

    return result_query.first()

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_mobility_result(id: int, db: Session = Depends(get_db)):

    result_query = db.query(models.MobilityResult).filter(models.MobilityResult.id == id)

    result = result_query.first()

    if result == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"result with id: {id} does not exist")

    result_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.get("/sub/{id}", response_model=schemas.MobilitySubResultOut)
def get_mobility_subresult(id: int, db: Session = Depends(get_db)):

    result = db.query(models.MobilitySubResult).filter(models.MobilitySubResult.id == id).first()

    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"result with id: {id} was not found")

    return result


@router.post("/sub", status_code=status.HTTP_201_CREATED, response_model=schemas.MobilitySubResultOut)
def create_mobility_subresult(mobility_result: schemas.MobilitySubResultCreate, db: Session = Depends(get_db)):

        # Create the MobilitySubResult object
    new_result = models.MobilitySubResult(
        mobility_result_id=mobility_result.mobility_result_id,
        sub_objective_id=mobility_result.sub_objective_id,
        target=mobility_result.target,
        impact=mobility_result.impact,
        spatial_impact=mobility_result.spatial_impact,
        annotation=mobility_result.annotation
    )
    
    db.add(new_result)
    db.commit()
    db.refresh(new_result)

    # Add associations with indicators
    if mobility_result.indicator_ids:
        indicators = db.query(models.Indicator).filter(models.Indicator.id.in_(mobility_result.indicator_ids)).all()
        new_result.indicators.extend(indicators)
    
    db.commit()
    db.refresh(new_result)

    return new_result

    # new_result = models.MobilitySubResult(**mobility_result.model_dump())
    # db.add(new_result)
    # db.commit()
    # db.refresh(new_result)

    # return new_result


@router.put("/sub/{id}", response_model=schemas.MobilitySubResultOut)
def update_mobility_subresult(id: int, updates: schemas.MobilitySubResultCreate, db: Session = Depends(get_db)):
    # Find the existing MobilitySubResult by ID
    existing_result = db.query(models.MobilitySubResult).filter(models.MobilitySubResult.id == id).first()

    if not existing_result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="MobilitySubResult not found")

    # Update the fields of the existing MobilitySubResult
    existing_result.mobility_result_id = updates.mobility_result_id
    existing_result.sub_objective_id = updates.sub_objective_id
    existing_result.target = updates.target
    existing_result.impact = updates.impact
    existing_result.spatial_impact = updates.spatial_impact
    existing_result.annotation = updates.annotation
    
    # Clear existing associations with indicators
    existing_result.indicators.clear()

    # Add new indicators
    if updates.indicator_ids:
        indicators = db.query(models.Indicator).filter(models.Indicator.id.in_(updates.indicator_ids)).all()
        existing_result.indicators = indicators
    
    db.commit()
    db.refresh(existing_result)

    return existing_result

@router.delete("/sub/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_mobility_subresult(id: int, db: Session = Depends(get_db)):

    result_query = db.query(models.MobilitySubResult).filter(models.MobilitySubResult.id == id)

    result = result_query.first()

    if result == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"result with id: {id} does not exist")

    result_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)