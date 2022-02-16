from fastapi import APIRouter,Depends, status, HTTPException, Response
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from ..database import get_db
from .. import schemas,models,utils, oauth2

router = APIRouter(tags=['Authentication'])

# FOR USING CUSTOM MODEL FOR LOGIN
# @router.post('/login')
# def login(user_cred: schemas.UserLogin,db: Session = Depends(get_db)):
#     user = db.query(models.User).filter(models.User.email == user_cred.email).first()
#     if not user:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#         detail="Invalid credential")
#     if not utils.verify(user_cred.password,user.password):
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#         detail="Invalid credential")
    
#     #creating jwt token
#     token = oauth2.create_access_token(data = {"user_id": user.id})
#     return {"token": token, "token_type":"bearer"}  

# FOR USING INBUILD FROM FOR LOGIN DATA
@router.post('/login', response_model=schemas.Token)
def login(user_cred: OAuth2PasswordRequestForm = Depends(),db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == user_cred.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
        detail="Invalid credential")
    if not utils.verify(user_cred.password,user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
        detail="Invalid credential")
    
    #creating jwt token
    token = oauth2.create_access_token(data = {"user_id": user.id})
    return {"access_token": token, "token_type":"bearer"}

