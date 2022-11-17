from functools import wraps
from sanic import json
from jsonschema import validate

def validation_required(json_schema):
    def wrapper(f):
        @wraps(f)
        def decorated(req,*args,**kwargs):
            json_req = req.json
            try:
                validate(instance=json_req,schema=json_schema)
                return f(req, *args, **kwargs)
            except Exception:
                return json({"msg" : "wrong schema"},400)
        return decorated
    return wrapper

def validation_new_post(f):
    @wraps(f)
    def decorated(req,*args,**kwargs):
        json_req = req.json
        post = json_req['content']
        if is_trailing_white_space(post) and is_length_max_1000(post):
            return f(req, *args, **kwargs)
        return json({"msg" : "not valid post"} , 400)
    return decorated
    
#check if there is traling white spaces 
def is_trailing_white_space(data):
    EMPTY_SPACE = ' '
    last_index = len(data)-1
    first_index = 0
    if data[first_index] == EMPTY_SPACE or data[last_index] == EMPTY_SPACE:
        return False
    for index in range(first_index, last_index):
        if (data[index] == EMPTY_SPACE and data[index+1] == EMPTY_SPACE):
            return False
    return True

# check if the length of input over 1000
def is_length_max_1000(data):
    MAXIMUM_NUMBER = 1000
    if len(data) > MAXIMUM_NUMBER:
        return False
    return True
