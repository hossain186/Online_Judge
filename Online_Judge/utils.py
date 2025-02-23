from passlib.context import CryptContext


pwd_context = CryptContext(schemes=["bcrypt"],deprecated = "auto")

def hash(password: str):
    
    hashed_password = pwd_context.hash(password)
    return hashed_password

def password_varify(password, userPass):
    
    return pwd_context.verify(password, userPass)