from fastapi import FastAPI ,Request, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from fastapi.routing import APIRouter
from .. import schema,models, database , utils
from . import auth
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

router = APIRouter(
    tags=["Authentication"]
)

@router.post("/login")
def user_login(user_credential: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_bd)):
    
    user = db.query(models.User).filter(models.User.email == user_credential.username).first()
    
    if not user:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail="User Not Found!")
    
    isPassValid = utils.password_varify(user_credential.password, user.password)
    
    if not isPassValid:
        
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Credential!")
    
    
    create_token = auth.create_access_token({"user_id": user.id})
    
    return {"token": create_token}
    
    
    
    




