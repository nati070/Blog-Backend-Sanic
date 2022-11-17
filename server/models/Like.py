from sqlalchemy import Integer,Boolean,ForeignKey,Column

from .BaseModel import BaseModel

class Like(BaseModel):
    
    __tablename__ = 'likes'
    userId = Column(Integer(),ForeignKey("users.id"))
    blogId = Column(Integer(),ForeignKey("blogs.id"))
    isLike = Column(Boolean())