from fastapi import FastAPI,Response, status, HTTPException, Depends, APIRouter
from ..database import get_db
from sqlalchemy.orm import Session
from .. import models,schemas,oauth2
from typing import List, Optional
from sqlalchemy import func


router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)

@router.get("/",response_model=List[schemas.PostResponsewithVotes])
def get_posts(db: Session = Depends(get_db),user = Depends(oauth2.get_currentUser),
limit: int = 10,skip:int = 0, search: Optional[str] = ""):
    # cursor.execute(""" SELECT * FROM posts """)
    # posts = cursor.fetchall()
    #result = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all() 
    posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote,
    models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    return posts


@router.post("/",status_code=status.HTTP_201_CREATED,response_model=schemas.PostResponse)
def create_post(post: schemas.PostCreate,db: Session = Depends(get_db),user = Depends(oauth2.get_currentUser)):
# def create_post(post: Post):
    # cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s)
    #  RETURNING * """,
    # (post.title, post.content, post.published))
    # new = cursor.fetchone() #feteches last commited data
    # conn.commit() #for postgresql we need to save the changes once sql is executed
    # new = models.Post(title=post.title, content=post.content, published=post.published)
    #instead of referering each object as post.title,post.content,etc just convert to dict and unpack it
    new = models.Post(owner_id=user.id,**post.dict())
    db.add(new)
    db.commit()
    db.refresh(new) 
    return new


@router.get("/{id}",response_model=schemas.PostResponsewithVotes)
def get_post(id: int,db: Session = Depends(get_db),user:int = Depends(oauth2.get_currentUser)):
    # cursor.execute("""SELECT * from posts WHERE id = %s""",(str(id)))
    # post = cursor.fetchone()
    # print(post)
    print(user.email)
    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote,
    models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        detail=f"post with id {id} not found")
    else:
        return post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int,db: Session = Depends(get_db),user:int = Depends(oauth2.get_currentUser)):
    # cursor.execute("""DELETE FROM posts WHERE id  = %s RETURNING *""",(str(id)))
    # post = cursor.fetchone()
    # conn.commit()
    post = db.query(models.Post).filter(models.Post.id == id)
    # if not post:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
    #     detail=f"post with id = {id} does not exist")
    # return Response(status_code=status.HTTP_204_NO_CONTENT)
    if not post.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        detail=f"post with id = {id} does not exist")
    if post.first().owner_id != user.id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Not authorized to perform requested action")
    post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}",response_model=schemas.PostResponse)
def update_post(id: int, postObj: schemas.PostCreate,db: Session = Depends(get_db)):
    # cursor.execute("""UPDATE posts SET title = %s, content=%s,published=%s WHERE id = %s RETURNING *""",
    # (post.title,post.content,post.published,str(id)))
    # post = cursor.fetchone()
    # conn.commit()
    query = db.query(models.Post).filter(models.Post.id == id)
    post = query.first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        detail=f"post with id = {id} does not exist")
    query.update(postObj.dict(),synchronized_session=False)
    db.commit()
    return post