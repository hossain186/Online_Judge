from sqlalchemy import create_engine
from  sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "postgresql://postgres:1234@localhost/FastApiPractice"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
sessoinlocal  = sessionmaker(autocommit = False, autoflush= False,bind=engine )

Base = declarative_base() 

def get_bd():
    
    db = sessoinlocal()
    try:
        yield db
    finally:
        db.close()