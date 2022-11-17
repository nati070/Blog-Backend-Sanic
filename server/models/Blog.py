from sqlalchemy import Column , String , ForeignKey,Integer,Text

from .BaseModel import BaseModel

class Blog(BaseModel):
    __tablename__ = 'blogs'
    
    authorId = Column(Integer() , ForeignKey("users.id"))
    title = Column(String())
    content = Column(Text(1000))


    def __str__(self) -> str:
        return f'id: {self.id}, author_id: {self.authorId}, title: {self.title} , content: {self.content}'

    def to_json(self):
        return {"id" : self.id , "author_id" : self.authorId , "title" : self.title , "content" : self.content}