from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import models, schemas, utils, oauth2
from ..database import get_db

router = APIRouter(
    prefix="/user",
    tags=['User']
)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):

    # hash the password - user.password
    hashed_password = utils.get_password_hash(user.password)
    user.password = hashed_password

    new_user = models.User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@router.get('/{id}', response_model=schemas.UserOut)
def get_user(id: int, 
             db: Session = Depends(get_db), 
             current_user: int = Depends(oauth2.get_current_user)):
    
    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with id: {id} does not exist")
    
    if id != current_user.id or current_user.role != 'admin':
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform requested action")
    
    return user

@router.put('/{id}', response_model=schemas.UserOut)
def update_user(id: int, 
                updates: schemas.UserCreate,
                db: Session = Depends(get_db), 
                current_user: int = Depends(oauth2.get_current_user)):
    
    user_query = db.query(models.User).filter(models.User.id == id)
    
    user = user_query.first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with id: {id} does not exist")
    print(current_user.role == "admin")
    
    if id == current_user.id:
        pass
    elif current_user.role == "admin":
        pass
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform requested action")
    
    user_query.update(**updates.model_dump(), synchronize_session=False)

    db.commit()

    return user_query.first()