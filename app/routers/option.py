from typing import List

from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models, schemas
from ..utils.fastapi_users import current_active_user
from ..utils.options import USER_ROLES
from ..utils.label import (CLIMATE_IMPACT_LABELS, 
                           CLIMATE_IMPACT_GHG_LABELS,
                           CLIMATE_IMPACT_DURATION_LABELS, 
                           MOBILITY_SPATIAL_IMPACT_LABELS, 
                           MOBILITY_IMPACT_TICKMARK_LABELS)


router = APIRouter(
    prefix="/option",
    tags=['option']
)

@router.get("/municipality",
            response_model=List[schemas.MunicipalityOut])
def get_municipality_options(db: Session = Depends(get_db)):

    municipalities = db.query(models.Municipality).all()

    return municipalities

@router.get('/user-role')
def get_user_role_options():

    return [{"label": label, "value": value} for value, label in USER_ROLES.items()]


@router.get("/climate/impact",
            dependencies=[Depends(current_active_user)])
def get_climate_impact_options():

    result = [{"label": label, "value": value} for value, label in CLIMATE_IMPACT_LABELS.items()]

    return result

@router.get("/climate/impact-ghg",
            dependencies=[Depends(current_active_user)])
def get_climate_impact_ghg_options():

    result = [{"label": label, "value": value} for value, label in CLIMATE_IMPACT_GHG_LABELS.items()]

    return result

@router.get("/climate/impact-duration", 
            dependencies=[Depends(current_active_user)])
def get_climate_impact_duration_options():

    result = [{"label": label, "value": value} for value, label in CLIMATE_IMPACT_DURATION_LABELS.items()]

    return result

@router.get("/mobility/spatial-impact", 
            dependencies=[Depends(current_active_user)])
def get_mobility_spatial_impact_options():

    result = [{"label": label, "value": value} for value, label in MOBILITY_SPATIAL_IMPACT_LABELS.items()]

    return result

@router.get("/mobility/impact-tickmarks", 
            dependencies=[Depends(current_active_user)])
def get_mobility_impact_tickmarks_options():

    result = [{"label": label, "value": value} for value, label in MOBILITY_IMPACT_TICKMARK_LABELS.items()]

    return result

