from typing import List
from fastapi import Response, status, HTTPException, Depends, APIRouter
from fastapi.responses import StreamingResponse
from sqlalchemy import desc, inspect
from sqlalchemy.orm import Session
from .. import models, schemas
from ..database import get_db
from ..utils.fpdf import FPDF
from ..utils.fastapi_users import current_active_user

router = APIRouter(
    prefix="/submission/mobility",
    tags=['Submission']
)

@router.get("", 
            response_model=List[schemas.MobilitySubmissionOut])
def get_mobility_submissions(db: Session = Depends(get_db), 
                             user: models.User = Depends(current_active_user)):

    submissions = (db.query(models.MobilitySubmission)
                   .filter(models.MobilitySubmission.municipality_id == user.municipality_id)
                   .order_by(desc(models.MobilitySubmission.created_at))
                   .all())

    if not submissions:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Mobility submissions were not found")

    return submissions

@router.post("/filter", 
             response_model=List[schemas.MobilitySubmissionOut])
def filter_mobility_submissions(filters: schemas.MobilitySubmissionFilter, 
                                db: Session = Depends(get_db),
                                user: models.User = Depends(current_active_user)):
    

    query = db.query(models.MobilitySubmission).filter(models.MobilitySubmission.municipality_id == user.municipality_id)

    if filters.by_user_role is not None:
        query = query.join(models.User, models.MobilitySubmission.created_by == models.User.id).filter(
            models.User.role == user.role
        )

    # Apply filters based on the provided filter attributes
    if filters.is_published is not None:
        query = query.filter(models.MobilitySubmission.is_published == filters.is_published)
    
    if filters.by_user_id:
        query = query.filter(models.MobilitySubmission.created_by == user.id)

    submissions = query.order_by(desc(models.MobilitySubmission.created_at)).all()

    if not submissions:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="No mobility submissions found matching the criteria.")

    return submissions

@router.get("/{id}", 
            response_model=schemas.MobilitySubmissionOut)
def get_mobility_submission(id: int, db: Session = Depends(get_db), 
                            user: models.User = Depends(current_active_user)):

    submission = (db.query(models.MobilitySubmission)
                  .filter(models.MobilitySubmission.id == id)
                  .first())

    if not submission:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Mobility submission with id: {id} was not found")
    
    if not (submission.municipality_id == user.municipality_id or user.is_superuser):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to get this submission")

    return submission

@router.post("/copy/{id}", 
             response_model=schemas.MobilitySubmissionOut)
def copy_submission(id: int, 
                    db: Session = Depends(get_db), 
                    user: models.User = Depends(current_active_user)):
    
    original_submission = db.query(models.MobilitySubmission).get(id)
    if not original_submission:
        raise ValueError("Submission with given ID does not exist")

    def detach_instance(instance):
        instance_copy = instance.__class__(**{c.key: getattr(instance, c.key) for c in inspect(instance).mapper.column_attrs})
        instance_copy.id = None
        return instance_copy

    copied_submission = detach_instance(original_submission)
    copied_submission.created_by = user.id
    copied_submission.last_edited_by = user.id
    copied_submission.is_published = False

    copied_submission.objectives = []
    for objective in original_submission.objectives:
        copied_objective = detach_instance(objective)
        copied_objective.submission = copied_submission

        copied_objective.sub_objectives = []
        for sub_objective in objective.sub_objectives:
            copied_sub_objective = detach_instance(sub_objective)
            copied_sub_objective.main_objective = copied_objective
            copied_objective.sub_objectives.append(copied_sub_objective)
        
        copied_submission.objectives.append(copied_objective)
    
    db.add(copied_submission)
    db.commit()
    
    return copied_submission

@router.get("/export/{id}")
def export_mobility_submission(id: int, 
                               db: Session = Depends(get_db),
                               user: models.User = Depends(current_active_user)):

    submission = (db.query(models.MobilitySubmission)
                  .filter(models.MobilitySubmission.id == id)
                  .first())

    if not submission:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Mobility submission with id: {id} was not found")
    
    if not (user.is_superuser or submission.municipality_id == user.municipality_id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to export this submission")
    
    pdf = FPDF(orientation='P', unit='mm', format='A4')
    submission_export = pdf.export_mobility_submission(submission)

    
    return StreamingResponse(submission_export, media_type='application/pdf', headers={"Content-Disposition": f"attachment; filename=klimacheck_{submission.id}.pdf"})

@router.post("", 
             status_code=status.HTTP_201_CREATED, 
             response_model=schemas.MobilitySubmissionOut)
def create_mobility_submission(submission: schemas.MobilitySubmissionCreate, 
                               db: Session = Depends(get_db),
                               user: models.User = Depends(current_active_user)):
    
    submission_dict = submission.model_dump()
    submission_dict['municipality_id'] = user.municipality_id
    submission_dict['created_by'] = user.id
    submission_dict['last_edited_by'] = user.id

    new_submission = models.MobilitySubmission(**submission_dict)
    db.add(new_submission)
    db.commit()
    db.refresh(new_submission)

    return new_submission

@router.patch("/{id}", 
            response_model=schemas.MobilitySubmissionOut)
def update_mobility_submission(id: int, 
                               updates: schemas.MobilitySubmissionUpdate, 
                               db: Session = Depends(get_db),
                               user: models.User = Depends(current_active_user)):

    submission_query = (db.query(models.MobilitySubmission)
                        .filter(models.MobilitySubmission.id == id))

    submission = submission_query.first()

    if submission == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Mobility Submission with id: {id} does not exist")
    
    if not (user.is_superuser or submission.municipality_id == user.municipality_id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to update this submission")
    
    updates_dict = updates.model_dump(exclude_unset=True)
    updates_dict['last_edited_by'] = user.id

    submission_query.update(updates_dict, synchronize_session=False)

    db.commit()

    return submission_query.first()

@router.delete("/{id}", 
               status_code=status.HTTP_204_NO_CONTENT)
def delete_mobility_submission(id: int, 
                               db: Session = Depends(get_db),
                               user: models.User = Depends(current_active_user)):

    submission_query = (db.query(models.MobilitySubmission)
                        .filter(models.MobilitySubmission.id == id))

    submission = submission_query.first()

    if submission == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Mobility Submission with id: {id} does not exist")
    
    if not (user.is_superuser or submission.municipality_id == user.municipality_id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to delete this submission")

    submission_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)