from sqlalchemy import Column , String , CHAR
from sqlalchemy.orm import declarative_base 

from .BaseModel import BaseModel

Base = declarative_base()

class User(BaseModel):
    __tablename__ = 'users'
    username = Column(String())
    password = Column(CHAR())

    def to_json(self):
        return {"username" : self.username , "password" : self.password , "id" : self.id}

    def __str__(self) -> str:
        return f'username": {self.username}, "password": {self.password}, id: {self.id}'

