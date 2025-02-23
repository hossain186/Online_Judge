from pydantic import BaseModel,EmailStr
from datetime import datetime



class Post(BaseModel):
    title : str
    content :str
    published: bool = True
    
class CreatePost(Post):
    pass 
class GetPost(BaseModel):

    id : int
    created_at : datetime
    title: str
    content : str
    
    class Config:
        from_attributes = True 

class User(BaseModel):
    
    email : EmailStr
    password : str
class GetUser(BaseModel):
    email:EmailStr
    id  : int
    created_at: datetime
    
    class Config:
        from_attributes = True 
    
    
class TokenData(BaseModel):
    
    id : int
    