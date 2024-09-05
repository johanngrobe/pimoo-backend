from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session

from sqlalchemy import func
# from sqlalchemy.sql.functions import func
from ..database import get_db
from ..utils.label import CLIMATE_IMPACT_LABELS, CLIMATE_IMPACT_GHG_LABELS,CLIMATE_IMPACT_DURATION_LABELS, MOBILITY_SPATIAL_IMPACT_LABELS, MOBILITY_IMPACT_TICKMARK_LABELS

router = APIRouter(
    prefix="/option",
    tags=['option']
)


@router.get("/climate/impact", )
def get_climate_impact_options(db: Session = Depends(get_db)):

    result = [{"label": label, "value": value} for value, label in CLIMATE_IMPACT_LABELS.items()]

    return result

@router.get("/climate/impact-ghg", )
def get_climate_impact_ghg_options(db: Session = Depends(get_db)):

    result = [{"label": label, "value": value} for value, label in CLIMATE_IMPACT_GHG_LABELS.items()]

    return result

@router.get("/climate/impact-duration", )
def get_climate_impact_duration_options(db: Session = Depends(get_db)):

    result = [{"label": label, "value": value} for value, label in CLIMATE_IMPACT_DURATION_LABELS.items()]

    return result

@router.get("/mobility/spatial-impact", )
def get_mobility_spatial_impact_options(db: Session = Depends(get_db)):

    result = [{"label": label, "value": value} for value, label in MOBILITY_SPATIAL_IMPACT_LABELS.items()]

    return result

@router.get("/mobility/impact-tickmarks", )
def get_mobility_impact_tickmarks_options(db: Session = Depends(get_db)):

    result = [{"label": label, "value": value} for value, label in MOBILITY_IMPACT_TICKMARK_LABELS.items()]

    return result

