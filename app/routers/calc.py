from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import models, schemas, oauth2
from .. import calc
from ..database import get_db

router = APIRouter(
    prefix="/calc",
    tags=['Calc']
)


@router.post("/parking_spaces", response_model=schemas.ParkingSpaces)
def calculate_parking_spaces(real_estate: schemas.RealEstateInfo, 
                             db: Session = Depends(get_db)):
    try:
        parking = calc.mainz_pkw(real_estate)
    except:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
    
    return parking

@router.post("/parking_spaces_full", response_model=schemas.ParkingSpacesFull)
def calculate_parking_spaces(real_estate: schemas.RealEstateInfo, 
                             db: Session = Depends(get_db), 
                             curent_user: schemas.UserOut = Depends(oauth2.get_current_user)):
    try:
        parking = calc.mainz_pkw(real_estate)
    except:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
    
    return parking

# @router.post("/bicycle_parking")
# def calculate_bicycle_parking(real_estate: Real_Estate):
#     try:
#         return mainz_fahrrad(real_estate)
#     except:
#         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)

# @router.post("/potential")
# def calculate_potential(parking_spaces: Parking_Spaces, city: Cities):
#     try:
#         return potential(parking_spaces, city)
#     except:
#         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)