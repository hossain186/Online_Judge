from jose import JWTError , jwt
from datetime import timedelta, datetime
from .. import schema, models, database
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException , status
from sqlalchemy.orm import Session


outh2_schema = OAuth2PasswordBearer(tokenUrl="login")
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

def create_access_token(data: dict):

    to_encode = data.copy()
    expire_time = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp":expire_time})
    
    jwt_encoded = jwt.encode(to_encode, SECRET_KEY , algorithm= ALGORITHM)
    
    return jwt_encoded
    
def varify_token(token : str, credential_exception):
    
    try:
        payload = jwt.decode(token , SECRET_KEY, algorithms=[ALGORITHM])

        user_id : int = payload.get("user_id")
        if not user_id :
            raise credential_exception
        
        token_data = schema.TokenData(id= user_id)
    except JWTError:
        
        raise credential_exception
    
    return token_data
        

def get_current_user(token: str = Depends(outh2_schema),db : Session = Depends(database.get_bd) ):

    credential_exeption = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Coundn't valided credential")
    token = varify_token(token, credential_exeption)
    user = db.query(models.User).filter(models.User.id == token.id).first() 
    return user
        
