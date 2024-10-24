from fastapi import Response, status, HTTPException, Depends, APIRouter
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from typing import List
from sqlalchemy import desc
from .. import models, schemas
from ..database import get_db
from ..utils.fpdf import FPDF

router = APIRouter(
    prefix="/submission",
    tags=['Submission']
)


@router.get("/mobility", response_model=List[schemas.MobilitySubmissionOut])
def get_mobility_submissions(db: Session = Depends(get_db)):

    submissions = db.query(models.MobilitySubmission).order_by(desc(models.MobilitySubmission.created_at)).all()

    if not submissions:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Mobility submissions were not found")

    return submissions

@router.get("/climate", response_model=List[schemas.ClimateSubmissionOut])
def get_climate_submissions(db: Session = Depends(get_db)):

    submissions = db.query(models.ClimateSubmission).order_by(desc(models.ClimateSubmission.created_at)).all()

    if not submissions:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Climate submissions were not found")

    return submissions

@router.get("/mobility/{id}", response_model=schemas.MobilitySubmissionOut)
def get_mobility_submission(id: int, db: Session = Depends(get_db)):

    submission = db.query(models.MobilitySubmission).filter(models.MobilitySubmission.id == id).first()

    if not submission:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Mobility submission with id: {id} was not found")

    return submission

@router.get("/mobility/export/{id}")
def export_mobility_submission(id: int, db: Session = Depends(get_db)):

    submission = db.query(models.MobilitySubmission).filter(models.MobilitySubmission.id == id).first()

    if not submission:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Mobility submission with id: {id} was not found")
    
    pdf = FPDF(orientation='P', unit='mm', format='A4')
    submission_export = pdf.export_mobility_submission(submission)

    
    return StreamingResponse(submission_export, media_type='application/pdf', headers={"Content-Disposition": f"attachment; filename=klimacheck_{submission.id}.pdf"})

@router.get("/climate/{id}", response_model=schemas.ClimateSubmissionOut)
def get_climate_submission(id: int, db: Session = Depends(get_db)):

    submission = db.query(models.ClimateSubmission).filter(models.ClimateSubmission.id == id).first()

    if not submission:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Climate submission with id: {id} was not found")

    return submission

@router.get("/climate/export/{id}")
def export_cliamte_submission(id: int, db: Session = Depends(get_db)):

    submission = db.query(models.ClimateSubmission).filter(models.ClimateSubmission.id == id).first()

    if not submission:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Climate submission with id: {id} was not found")
    
    pdf = FPDF(orientation='P', unit='mm', format='A4')
    submission_export = pdf.export_climate_submission(submission)

    
    return StreamingResponse(submission_export, media_type='application/pdf', headers={"Content-Disposition": f"attachment; filename=klimacheck_{submission.id}.pdf"})


@router.post("/mobility", status_code=status.HTTP_201_CREATED, response_model=schemas.MobilitySubmissionOut)
def create_indicator(submission: schemas.MobilitySubmissionCreate, db: Session = Depends(get_db)):

    new_submission = models.MobilitySubmission(**submission.model_dump())
    db.add(new_submission)
    db.commit()
    db.refresh(new_submission)

    return new_submission

@router.post("/climate", status_code=status.HTTP_201_CREATED, response_model=schemas.ClimateSubmissionOut)
def create_indicator(submission: schemas.ClimateSubmissionCreate, db: Session = Depends(get_db)):

    new_submission = models.ClimateSubmission(**submission.model_dump())
    db.add(new_submission)
    db.commit()
    db.refresh(new_submission)

    return new_submission


@router.put("/mobility/{id}", response_model=schemas.MobilitySubmissionOut)
def update_mobility_submission(id: int, updates: schemas.MobilitySubmissionCreate, db: Session = Depends(get_db)):

    submission_query = db.query(models.MobilitySubmission).filter(models.MobilitySubmission.id == id)

    submission = submission_query.first()

    if submission == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Mobility Submission with id: {id} does not exist")

    submission_query.update(updates.model_dump(), synchronize_session=False)

    db.commit()

    return submission_query.first()

@router.put("/climate/{id}", response_model=schemas.ClimateSubmissionOut)
def update_climate_submission(id: int, updates: schemas.ClimateSubmissionCreate, db: Session = Depends(get_db)):

    submission_query = db.query(models.ClimateSubmission).filter(models.ClimateSubmission.id == id)

    submission = submission_query.first()

    if submission == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Climate Submission with id: {id} does not exist")

    submission_query.update(updates.model_dump(), synchronize_session=False)

    db.commit()

    return submission_query.first()

@router.delete("/mobility/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_mobility_submission(id: int, db: Session = Depends(get_db)):

    submission_query = db.query(models.MobilitySubmission).filter(models.MobilitySubmission.id == id)

    submission = submission_query.first()

    if submission == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Mobility Submission with id: {id} does not exist")

    submission_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.delete("/climate/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_climate_submission(id: int, db: Session = Depends(get_db)):

    submission_query = db.query(models.ClimateSubmission).filter(models.ClimateSubmission.id == id)

    submission = submission_query.first()

    if submission == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Climate Submission with id: {id} does not exist")

    submission_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)