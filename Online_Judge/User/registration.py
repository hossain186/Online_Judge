from fastapi.routing import APIRouter
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException , status
from .. import database, models, schema
from .. import utils

router = APIRouter(
    tags= ["User"]
)

@router.post("/registration", status_code=status.HTTP_201_CREATED, response_model=schema.GetUser)
def create_user(user: schema.User, db: Session = Depends(database.get_bd)):

    get_user = db.query(models.User).filter(models.User.email == user.email).first()
    
    if get_user:
        
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already exists. Please use a different email."
        )
    
    new_user = models.User(**user.dict())
    password = utils.hash(user.password)
    new_user.password = password
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return new_user
    
    
    
    
    
