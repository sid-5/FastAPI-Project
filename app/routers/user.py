from fastapi import FastAPI,Response, status, HTTPException, Depends, APIRouter
from ..database import get_db
from sqlalchemy.orm import Session
from .. import models,schemas,utils

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

@router.post("/",status_code=status.HTTP_201_CREATED, response_model=schemas.UserResponse)
def create_user(user: schemas.UserCreate,db: Session = Depends(get_db)):
    
    passw = utils.hash(user.password)
    user.password = passw
    new = models.User(**user.dict())
    db.add(new)
    db.commit()
    db.refresh(new)
    return new 


@router.get('/{id}',response_model= schemas.UserResponse)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        detail="user not found")
    return user