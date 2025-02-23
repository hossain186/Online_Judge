
from fastapi.routing import APIRouter
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status, Response
from typing import List

from ..User import auth
from .. import database, schema, models

router  = APIRouter(
    tags=["Posts"]
)

@router.get("/posts", response_model= List[schema.GetPost])
def get_posts(db: Session = Depends(database.get_bd)):
    
    all_post = db.query(models.Post).all()
    
    return all_post
    
@router.get("/posts/{id}", response_model=schema.GetPost)
def get_post_by_id(id : int , db:Session = Depends(database.get_bd)):
    
    post = db.query(models.Post).filter(models.Post.id == id).first()
    
    if not post:
        
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail="Post not found")
    
    return post    




@router.post("/create",response_model= schema.GetPost)
def create_post(post: schema.CreatePost, db: Session = Depends(database.get_bd), user_id : int = Depends(auth.get_current_user)):
    
    new_post  = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    
    db.refresh(new_post)
    
    return new_post
    
    
@router.delete("/delete/{id}",status_code= status.HTTP_204_NO_CONTENT)
def delete_post(id: int ,db: Session = Depends(database.get_bd)):
    post = db.query(models.Post).filter(models.Post.id == id)
    
    if not post.first():
        
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail="Post not found")
    
    post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
    
@router.put("/update/{id}")
def update_by_id(id : int, post : schema.Post, db : Session =  Depends(database.get_bd)):

    updated_post  = db.query(models.Post).filter(models.Post.id ==id)
    
    if updated_post.first() is None:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail="Post not found")
    
    updated_post.update(post.dict(), synchronize_session=False)
    db.commit()
    return updated_post.first()
        
    
    
    
    
    


