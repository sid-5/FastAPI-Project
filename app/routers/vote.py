from ssl import SSL_ERROR_SSL
from this import d
from fastapi import FastAPI,Response, status, HTTPException, Depends, APIRouter
from .. import database,schemas,models,oauth2
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/vote",
    tags = ['Vote'])

@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(vote: schemas.Vote, db: Session = Depends(database.get_db), user = Depends(oauth2.get_currentUser)):
    post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()
    if not post:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,
        detail=f"post with id {vote.post_id} does not exists")
    query = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id, models.Vote.user_id == user.id)
    found_vote = query.first()
    if(vote.dir==1):
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
            detail=f"User {user.id} has already voted on post {vote.post_id}")
        new_vote = models.Vote(post_id= vote.post_id, user_id = user.id)
        db.add(new_vote)
        db.commit()
        return {"message":"successfully voted"}
    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
            detail="Vote does not exist")
        query.delete(synchronize_session=False)
        db.commit()
        return {"message": "successfully deleted vote"}

        
        

