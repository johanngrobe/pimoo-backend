from typing import List
from fastapi import Response, status, HTTPException, Depends, APIRouter
from fastapi.responses import StreamingResponse
from sqlalchemy import desc, inspect
from sqlalchemy.orm import Session
from .. import models, schemas
from ..database import get_db
from ..utils.fpdf import FPDF
from ..utils.fastapi_users import current_active_user
from datetime import datetime

router = APIRouter(
    prefix="/submission",
    tags=['Submission']
)

@router.get("/climate", 
            response_model=List[schemas.ClimateSubmissionOut])
def get_climate_submissions(db: Session = Depends(get_db), 
                            user: models.User = Depends(current_active_user)):

    submissions = (db.query(models.ClimateSubmission)
                   .filter(models.ClimateSubmission.municipality_id == user.municipality_id)
                   .order_by(desc(models.ClimateSubmission.created_at))
                   .all())

    if not submissions:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Climate submissions were not found")

    return submissions

@router.post("/climate/filter", 
             response_model=List[schemas.ClimateSubmissionOut])
def filter_mobility_submissions(filters: schemas.ClimateSubmissionFilter, 
                                db: Session = Depends(get_db),
                                user: models.User = Depends(current_active_user)):
    

    query = db.query(models.ClimateSubmission).filter(models.ClimateSubmission.municipality_id == user.municipality_id)

    if filters.by_user_role is not None:
        query = query.join(models.User, models.ClimateSubmission.created_by == models.User.id).filter(
            models.User.role == user.role
        )

    # Apply filters based on the provided filter attributes
    if filters.is_published is not None:
        query = query.filter(models.ClimateSubmission.is_published == filters.is_published)
    
    if filters.by_user_id:
        query = query.filter(models.ClimateSubmission.created_by == user.id)

    submissions = query.order_by(desc(models.ClimateSubmission.created_at)).all()

    if not submissions:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="No climate submissions found matching the criteria.")

    return submissions

@router.get("/climate/{id}", 
            response_model=schemas.ClimateSubmissionOut)
def get_climate_submission(id: int, db: Session = Depends(get_db),
                           user: models.User = Depends(current_active_user)):

    submission = (db.query(models.ClimateSubmission)
                  .filter(models.ClimateSubmission.id == id)
                  .first())

    if not submission:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Climate submission with id: {id} was not found")

    if not (user.is_superuser or submission.municipality_id == user.municipality_id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to get this submission")

    return submission


@router.post("/climate/copy/{id}",
             response_model=schemas.ClimateSubmissionOut)
def copy_climate_submission(id: int, 
                            db: Session = Depends(get_db),
                            user: models.User = Depends(current_active_user)):

    original_submission = db.query(models.ClimateSubmission).get(id)
    if not original_submission:
        raise HTTPException(status_code=404, detail="Submission with given ID does not exist")

    # Create a copy without primary key and timestamps
    def detach_instance(instance):
        instance_copy = instance.__class__(**{
            c.key: getattr(instance, c.key)
            for c in inspect(instance).mapper.column_attrs
            if c.key != 'id' and c.key != 'created_at'
        })
        return instance_copy

    # Create a copy of the ClimateSubmission instance
    copied_submission = detach_instance(original_submission)
    copied_submission.created_by = user.id  # Set the new creator
    copied_submission.last_edited_by = user.id  # Set the new last editor
    copied_submission.is_published = False # Set the new creation date

    # Add and commit the copied submission to the session
    db.add(copied_submission)
    db.commit()
    
    return copied_submission

@router.get("/climate/export/{id}")
def export_cliamte_submission(id: int, 
                              db: Session = Depends(get_db),
                              user: models.User = Depends(current_active_user)):

    submission = (db.query(models.ClimateSubmission)
                  .filter(models.ClimateSubmission.id == id)
                  .first())

    if not submission:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Climate submission with id: {id} was not found")
    
    if not (user.is_superuser or submission.municipality_id == user.municipality_id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to export this submission")
    
    pdf = FPDF(orientation='P', unit='mm', format='A4')
    submission_export = pdf.export_climate_submission(submission)

    
    return StreamingResponse(submission_export, media_type='application/pdf', headers={"Content-Disposition": f"attachment; filename=klimacheck_{submission.id}.pdf"})

@router.post("/climate", 
             status_code=status.HTTP_201_CREATED, 
             response_model=schemas.ClimateSubmissionOut)
def create_climate_submission(submission: schemas.ClimateSubmissionCreate, 
                              db: Session = Depends(get_db),
                              user: models.User = Depends(current_active_user)):
    
    submission_dict = submission.model_dump()
    submission_dict['municipality_id'] = user.municipality_id
    submission_dict['created_by'] = user.id
    submission_dict['last_edited_by'] = user.id
    

    new_submission = models.ClimateSubmission(**submission_dict)
    

    db.add(new_submission)
    db.commit()
    db.refresh(new_submission)

    return new_submission

@router.patch("/climate/{id}", 
            response_model=schemas.ClimateSubmissionOut)
def update_climate_submission(id: int, 
                              updates: schemas.ClimateSubmissionUpdate, 
                              db: Session = Depends(get_db),
                              user: models.User = Depends(current_active_user)):

    submission_query = (db.query(models.ClimateSubmission)
                        .filter(models.ClimateSubmission.id == id))

    submission = submission_query.first()

    if submission == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Climate Submission with id: {id} does not exist")
    
    if not (user.is_superuser or submission.municipality_id == user.municipality_id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to update this submission")

    submission_query.update(updates.model_dump(exclude_unset=True), synchronize_session=False)

    db.commit()

    return submission_query.first()

@router.delete("/climate/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_climate_submission(id: int, 
                              db: Session = Depends(get_db),
                              user: models.User = Depends(current_active_user)):

    submission_query = (db.query(models.ClimateSubmission)
                        .filter(models.ClimateSubmission.id == id))
    
    submission = submission_query.first()

    if submission == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Climate Submission with id: {id} does not exist")
    
    if not (user.is_superuser or submission.municipality_id == user.municipality_id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to delete this submission")

    submission_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)