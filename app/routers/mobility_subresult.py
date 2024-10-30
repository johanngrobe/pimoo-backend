from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import models, schemas
from ..database import get_db
from ..utils.fastapi_users import current_active_user

router = APIRouter(
    prefix="/mobility-result",
    tags=['Mobility Result']
)

@router.get("/sub/{id}", 
            response_model=schemas.MobilitySubResultOut,
            dependencies=[Depends(current_active_user)])
def get_mobility_subresult(id: int, 
                           db: Session = Depends(get_db)):

    result = (db.query(models.MobilitySubresult)
              .filter(models.MobilitySubresult.id == id)
              .first())
    
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"result with id: {id} was not found")

    return result


@router.post("/sub", 
             status_code=status.HTTP_201_CREATED, 
             response_model=schemas.MobilitySubResultOut,
             dependencies=[Depends(current_active_user)])
def create_mobility_subresult(mobility_result: schemas.MobilitySubResultCreate, 
                              db: Session = Depends(get_db)):

        # Create the MobilitySubResult object
    new_result = models.MobilitySubresult(
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

@router.patch("/sub/{id}", 
            response_model=schemas.MobilitySubResultOut,
            dependencies=[Depends(current_active_user)])
def update_mobility_subresult(id: int, 
                              updates: schemas.MobilitySubResultUpdate, 
                              db: Session = Depends(get_db)):
    
    # Fetch existing result with related indicators to reduce subsequent queries
    existing_result = db.query(models.MobilitySubresult).filter(models.MobilitySubresult.id == id).first()

    if not existing_result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="MobilitySubResult not found")

    # Update main fields, excluding indicator_ids
    update_data = updates.model_dump(exclude_unset=True, exclude={'indicator_ids'})
    for field, value in update_data.items():
        setattr(existing_result, field, value)

    # Update indicators association only if indicator_ids is provided
    if updates.indicator_ids is not None:
        existing_result.indicators.clear()

        indicators = db.query(models.Indicator).filter(models.Indicator.id.in_(updates.indicator_ids)).all()
        existing_result.indicators = indicators

    db.commit()
    db.refresh(existing_result)

    return existing_result

@router.delete("/sub/{id}", 
               status_code=status.HTTP_204_NO_CONTENT,
               dependencies=[Depends(current_active_user)])
def delete_mobility_subresult(id: int, 
                              db: Session = Depends(get_db)):

    result_query = (db.query(models.MobilitySubresult)
                    .filter(models.MobilitySubresult.id == id))

    result = result_query.first()

    if result == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"result with id: {id} does not exist")

    result_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)