from decouple import config

#db_settings
DB_HOST = config('DB_HOST')
DB_NAME = config('DB_NAME')
DB_PASS = config('DB_PASS')

#jwt token 
JWT_SECRET = config('JWT_SECRET')
JWT_ALGORITHM = config('JWT_ALGORITHM')
JWT_EXP_DELTA_SECONDS = config('JWT_EXP_DELTA_SECONDS')


########## JSON SCHEMA ##########

login_schema = {
    "type": "object",
    "properties": {
        "username": {"type": "string" , "pattern" : "^[A-Za-z0-9_-]{3,}$"},
        "password": {"type": "string" , "pattern" : "^[A-Za-z0-9_-]{3,}$" },
    },
     "required": ["username", "password"],
     "additionalProperties": False
}
sign_up_schema = login_schema

like_schema = {
    "type": "object",
    "properties": {
        "is_like": {"type": "boolean"},
    },
    "required": ["is_like"],
    "additionalProperties": False
}

post_schema = {
 "type": "object",
    "properties": {
        "title": {"type": "string", "pattern" : "^[ A-Za-z0-9]{5,}$"},
        "content": {"type": "string"},
    },
    "required": ["title","content"],
    "additionalProperties": False
}

edit_schema = post_schema 

