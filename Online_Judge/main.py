
from fastapi import FastAPI, Depends,HTTPException, status, Response
from .database import engine , get_bd
from sqlalchemy.orm import Session
from . import models
from .Post import post
from .User import registration, login


app = FastAPI()

models.Base.metadata.create_all(bind= engine)

app.include_router(post.router)
app.include_router(registration.router)
app.include_router(login.router)

@app.get("/")
def home():
    
    return {"Message" :"Welcome to home page!"}



