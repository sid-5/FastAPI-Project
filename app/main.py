from fastapi import FastAPI, Depends
from . import models
from .database import engine, get_db
from sqlalchemy.orm import Session
from .routers import user,post,auth,vote
from fastapi.middleware.cors import CORSMiddleware


models.Base.metadata.create_all(bind=engine)


app = FastAPI()

origins = ["h"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

#First test route
@app.get("/")
async def root():
    return {"message": "Hello World"}

#sqlalchemy test route
@app.get("/sqlalc")
def test(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return {"Data": posts}


