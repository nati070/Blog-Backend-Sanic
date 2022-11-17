
from sanic import Blueprint,json,empty
from datetime import datetime,timedelta
from sanic_openapi import openapi
import jwt

from config import JWT_ALGORITHM,JWT_SECRET,JWT_EXP_DELTA_SECONDS,login_schema
from dals.users import get_user  ,ErrorUserNotExist
from helpers.auth import is_passwords_match
from helpers.valid import validation_required
from models_swagger import Login


bp = Blueprint("login")

@bp.post('/login')
@openapi.summary("log in")
@openapi.body(
    { "application/json" : Login },
    description="Body description",
    required=True,
)
@openapi.response(status=403,description="Incorecrt password",content="")
@openapi.response(status=409,description="A user not found.",content="")
@openapi.response(status=200,description="OK:user login",content="")
@openapi.response(status=400,description="Incorecrt input",content="")
@validation_required(login_schema)
async def login(req):
    data = req.json
    try:
        user_data = await get_user(data['username'],req.ctx.session) 
        if not user_data:
            raise ErrorUserNotExist
    except ErrorUserNotExist:
        return empty(409)
    except Exception:
       return empty(500)

    # compare hash password
    user_json = user_data.to_json()

    if not is_passwords_match(data['password'],user_json['password']):
        return empty(403)

    payload = {
        'user_id' : user_json['id'] ,
        'exp' : datetime.utcnow() + timedelta(seconds=int(JWT_EXP_DELTA_SECONDS))
    }
    token_encode = jwt.encode(payload,JWT_SECRET,JWT_ALGORITHM)
    return json({'token' : token_encode},201)