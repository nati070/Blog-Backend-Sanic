
from sqlalchemy import select

from models.User import User

#### Errors #### 

class ErrorIsUserExist(Exception):
    pass
class ErrorCreateUser(Exception):
    pass
class ErrorUserExist(Exception):
    pass
class ErrorUserNotExist(Exception):
    pass
class ErrorFindUserById(Exception):
    pass
class ErrorGetUser(Exception):
    pass

################ 

async def get_user(username,session):
    try:
        async with session.begin():
            stmt = select(User).where(User.username == username)
            user = await session.execute(stmt)
            if not user:
               return None
            return user.scalar()
    except Exception:
        raise ErrorGetUser

async def find_user_by_id(id,session):
    try:
        async with session.begin():
            stmt = select(User).where(User.id==id)
            user = await session.execute(stmt)
            if not user:
                return None
            return user.scalar()
    except Exception:
        raise ErrorFindUserById
    
async def is_user_exist(username,session):
    try:
        user = await get_user(username,session)
        if user == None:
            return False
        return True
    except Exception:
        raise ErrorIsUserExist

async def create_user(username , password , session):
    try:
        async with session.begin():
            user = User(username=username , password=password)  
            session.add(user)
    except Exception:
        raise ErrorCreateUser







        
    