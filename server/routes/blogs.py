from sanic import Blueprint,json,empty
from sanic_openapi import openapi

from config import like_schema, post_schema,edit_schema

from helpers.auth import token_required
from helpers.valid import validation_required,validation_new_post

from dals.blogs import create_post,delete_post,edit_post,get_post_by_title,get_all_posts,get_post ,ErrorCreatePost , ErrorDeletePost,ErrorPostNotExist,ErrorUserNotAllowed,ErrorPostExist
from dals.likes import set_like_post , ErrorUpdateLikePost

from models_swagger import Blog,Like,PostBlog

bp = Blueprint("blogs" , url_prefix='blogs')

@bp.get('/')
@openapi.summary("get all blogs")
@openapi.response(200, {"application/json" : [Blog]})
async def get_all_blog_req(req):
    session = req.ctx.session
    try:
        posts = await get_all_posts(session)
        posts_json = [post.to_json() for post in posts]
        return json({"posts": posts_json},200)
    except ErrorPostNotExist: 
        return empty(409) 
    except Exception:
        return empty(500)


@bp.get('/<blog_id:int>')
@openapi.summary("get blog by blog id")
@openapi.response(status=200,description = "OK: get blog" ,content={"application/json" : Blog})
@openapi.response(status=409,description="A blog with the specified ID was not found.",content="")
async def get_blog_by_id_req(req,blog_id: int):
    session = req.ctx.session
    try:
        post = await get_post(blog_id,session)
        return json(post.to_json() , 200)
    except ErrorPostNotExist: 
        return empty(409) 
    except Exception:
        return empty(500)

@bp.put('/<blog_id:int>/like')
@openapi.summary("like or dislike from user")
@openapi.body(
    { "application/json" : Like },
    description="Body description",
    required=True,
)
@openapi.parameter(name='x-access-token' , location='header' , schema=str,required=True)
@openapi.response(status=400,description="Bad request",content="")
@openapi.response(status=401,description="Unauthorized: token invalid",content="")
@openapi.response(status=200,description = "OK: like update/create" ,content={})
@validation_required(like_schema)
@token_required
async def is_like_req(req,user,blog_id:int):
    data = req.json
    session = req.ctx.session
    try:
        await set_like_post(user.id,blog_id,data['is_like'],session)
        return empty(200)
    except ErrorUpdateLikePost:
       return empty(400)
    except Exception:
        return empty(500)


@bp.put('/add-post')
@openapi.summary("new post")
@openapi.parameter(name='x-access-token' , location='header' , schema=str,required=True)
@openapi.body(
    { "application/json" : PostBlog },
    description="Body description",
    required=True,
)
@openapi.response(status=201,description="OK: post created" ,content={})
@openapi.response(status=409,description="Conflict: already created",content={})
@openapi.response(status=400,description="Incorecrt input",content="")
@openapi.response(status=401,description="Unauthorized",content="")
@validation_required(post_schema)
@validation_new_post
@token_required
async def add_post_req(req,user):
    data = req.json
    session = req.ctx.session
    try: 
        blog = await get_post_by_title(data['title'],session)
        if blog:
            raise ErrorPostExist
        await create_post(user.id,data['title'],data['content'],req.ctx.session)
        return empty(204)
    except ErrorPostExist:
        return empty(409)
    except Exception:
        return json({"msg" : "there is a problem with the server"},500)

@bp.delete('/delete-post/<blog_id:int>')
@openapi.summary("delete post")
@openapi.parameter(name='x-access-token' , location='header' , schema=str,required=True)
@openapi.response(status=204,description = "OK: post deleted successfully" ,content={})
@openapi.response(status=401,description="Unauthorized",content="")
@openapi.response(status=404,description="A user with the specified ID was not found.",content={})
@token_required
async def delete_post_req(req,user,blog_id:int):
    session = req.ctx.session
    try:
        blog = await get_post(blog_id,session)
        if not blog:
            raise ErrorPostNotExist
        if user.id != blog.authorId:
            raise ErrorUserNotAllowed
        await delete_post(blog_id,user.id,session)
        return empty(204)
    except ErrorUserNotAllowed:
        return empty(401)
    except ErrorPostNotExist:
        return empty(404)
    except Exception:
        return empty(500)


@bp.put('/edit-post/<blog_id:int>')
@openapi.summary("edit post")
@openapi.parameter(name='x-access-token' , location='header' , schema=str,required=True)
@openapi.response(status=204,description = "OK: post deleted successfully" ,content={})
@openapi.response(status=401,description="Unauthorized",content="")
@openapi.response(status=404,description="A user with the specified ID was not found.",content={})
@validation_required(edit_schema)
@validation_new_post
@token_required
async def edit_post_req(req,user,blog_id:int):
    session = req.ctx.session
    json_blog = req.json
    try:
        blog = await get_post(blog_id,session)
        if not blog:
            raise ErrorPostNotExist
        if user.id != blog.authorId:
            raise ErrorUserNotAllowed 
        await edit_post(blog_id,user.id,json_blog['title'],json_blog['content'],session)
        return empty(204)
    except ErrorPostNotExist:
        return empty(404)
    except ErrorUserNotAllowed:
        return empty(401)
    except Exception:
        return empty(500)


