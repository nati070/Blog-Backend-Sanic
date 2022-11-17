
from sanic import Blueprint,json,empty
from sanic_openapi import openapi
from dals.users import create_user , is_user_exist ,ErrorUserExist
from helpers.auth import hash_password 
from helpers.valid import validation_required
from config import sign_up_schema
from models_swagger import Login

bp = Blueprint("sign-up")

@bp.route('/create-user' , ['PUT'])
@openapi.summary("log in")
@openapi.body(
    { "application/json" : Login },
    description="Body description",
    required=True,
)

@openapi.response(status=400,description="Incorecrt input muse have more then 3 char",content="")
@openapi.response(status=409,description="A user already exist.",content="")
@openapi.response(status=201,description="OK: user created",content="")
@validation_required(sign_up_schema)
async def add_user_req(req):
    data = req.json
    session = req.ctx.session
    password = hash_password(data['password'].encode('utf-8'))
    try:
        if await is_user_exist(data['username'],session):
            raise ErrorUserExist
        await create_user(username=data['username'],password=password,session=session)
        return empty(201)
    except ErrorUserExist:
        return empty(409)
    except Exception:
        return json({"msg" : "there is a problem with the server"} , 500)