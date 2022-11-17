from sqlalchemy import select,delete,update,exc

from models.Blog import Blog

#### Errors #### 

class ErrorUserNotAllowed(Exception):
    pass
class ErrorCreatePost(Exception):
    pass
class ErrorDeletePost(Exception):
    pass
class ErrorUpdatePost(Exception):
    pass
class ErrorGetAllPosts(Exception):
    pass
class ErrorPostNotExist(Exception):
    pass
class ErrorPostExist(Exception):
    pass

################ 

async def get_all_posts(session):
    try:
        async with session.begin():
            stmt = select(Blog).where()
            posts = await session.execute(stmt)
            if not posts:
                raise ErrorPostNotExist
            return [post for (post,) in posts]
    except ErrorPostNotExist:
        raise ErrorPostNotExist
    except Exception:
        raise ErrorGetAllPosts

async def get_post(blog_id , session):
    try:
        async with session.begin():
            stmt = select(Blog).where(Blog.id == blog_id)
            blog = (await session.execute(stmt)).scalar()
            if not blog:
                raise ErrorPostNotExist
            return blog
    except ErrorPostNotExist:
        raise ErrorPostNotExist
    except Exception as e:
        raise ErrorGetAllPosts

async def get_post_by_title(title , session):
    try:
        async with session.begin():
            stmt = select(Blog).where(Blog.title == title)
            blog = await session.execute(stmt)
            if not blog:
                raise ErrorPostNotExist
            return blog.scalar()
    except ErrorPostNotExist as e:
        raise ErrorPostNotExist
    except Exception as e:
        raise ErrorGetAllPosts

async def create_post(author_id,title,content,session):
    try:
        async with session.begin():   
            blog = Blog(authorId=author_id,title=title,content=content)
            session.add(blog)
    except Exception as e:
        raise ErrorCreatePost 

async def delete_post(blog_id,user_id,session):
    try:
        async with session.begin():
            stmt = delete(Blog).where(Blog.id==blog_id)
            await session.execute(stmt)
    except Exception as e:
        raise ErrorDeletePost

async def edit_post(blog_id,author_id,title,content,session):
    try:
        async with session.begin():
            stmt = update(Blog).where(Blog.id == blog_id).values(authorId=author_id,title=title,content=content)
            await session.execute(stmt)
    except Exception as e:
        raise ErrorUpdatePost


