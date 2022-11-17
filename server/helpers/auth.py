import jwt
from functools import wraps
from sanic.response import json
import bcrypt

from dals.users import find_user_by_id,ErrorFindUserById

#### Errors #### 

class ErrorTokenMissing(Exception):
    pass
class ErrorUserNotHaveToken(Exception):
    pass
class ErrorTokenRequired(Exception):
    pass
class ErrorIleagelToken(Exception):
    pass

################


def token_required(f):
    @wraps(f)
    async def decorated(req, *args,**kwargs):
        token = None
        try:
            if 'x-access-token' in req.headers:
                token = req.headers['x-access-token']
            if not token:
                raise ErrorTokenMissing
            session = req.ctx.session 
            user_decode = jwt.decode(token,'secret','HS256')
            user = await find_user_by_id(user_decode['user_id'],session)
            if(not user):
                raise ErrorUserNotHaveToken
            return await f(req,user, *args, **kwargs)
        except jwt.InvalidTokenError: 
            return json({"msg": "invalid token"} , 401)
        except ErrorTokenMissing:
            return json({"msg": "token missing"} , 401)
        except Exception:
            raise ErrorFindUserById
    return decorated

def hash_password(password):
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password,salt) 
    return hashed


def is_passwords_match(pass_req,pass_db):
    pass_db =  pass_db.encode('utf-8')
    pass_req =  pass_req.encode('utf-8')
    return bcrypt.checkpw(pass_req,pass_db)

