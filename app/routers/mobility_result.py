from typing import List
from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import models, schemas
from ..database import get_db
from ..utils.fastapi_users import current_active_user

router = APIRouter(
    prefix="/mobility-result",
    tags=['Mobility Result']
)

@router.get("", 
            response_model=List[schemas.MobilityResultOut],
            dependencies=[Depends(current_active_user)])
def get_mobility_results(db: Session = Depends(get_db)):

    result = (db.query(models.MobilityResult)
              .filter(models.MobilityResult.id == id)
              .all())
    
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"indicator were not found")

    return result

@router.get("/{id}", 
            response_model=schemas.MobilityResultOut,
            dependencies=[Depends(current_active_user)])
def get_mobility_result(id: int, 
                        db: Session = Depends(get_db)):

    result = (db.query(models.MobilityResult)
              .filter(models.MobilityResult.id == id)
              .first())

    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"result with id: {id} was not found")

    return result


@router.post("", 
             status_code=status.HTTP_201_CREATED,
             dependencies=[Depends(current_active_user)])
def create_mobility_result(mobility_result: schemas.MobilityResultCreate, 
                           db: Session = Depends(get_db)):

    new_result = models.MobilityResult(**mobility_result.model_dump())
    db.add(new_result)
    db.commit()
    db.refresh(new_result)

    return new_result


@router.patch("/{id}", 
            response_model=schemas.MobilityResultOut,
            dependencies=[Depends(current_active_user)])
def update_mobility_result(id: int, 
                           updates: schemas.MobilityResultUpdate, 
                           db: Session = Depends(get_db)):

    result_query = (db.query(models.MobilityResult)
                    .filter(models.MobilityResult.id == id))

    result = result_query.first()

    if result == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"result with id: {id} does not exist")

    result_query.update(updates.model_dump(exclude_unset=True), synchronize_session=False)

    db.commit()

    return result_query.first()

@router.delete("/{id}",
               status_code=status.HTTP_204_NO_CONTENT,
               dependencies=[Depends(current_active_user)])
def delete_mobility_result(id: int,
                           db: Session = Depends(get_db)):

    result_query = (db.query(models.MobilityResult)
                    .filter(models.MobilityResult.id == id))

    result = result_query.first()

    if result == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"result with id: {id} does not exist")

    result_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)