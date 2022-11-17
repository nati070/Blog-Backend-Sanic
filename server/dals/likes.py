from sqlalchemy import select,update

from models.Like import Like 

#### Errors #### 

class ErrorUpdateLikePost(Exception):
    pass

################

async def set_like_post(user_id,blog_id,is_like,session):
    try:
        async with session.begin():
            stmt = select(Like).where(Like.userId == user_id,Like.blogId==blog_id)
            likes = (await session.execute(stmt)).scalar()
            if not likes:
                like = Like(userId = user_id,blogId = blog_id,isLike = is_like)
                session.add(like)
            else:
                stmt = update(Like).where(Like.userId == user_id,Like.blogId==blog_id).values(isLike = is_like)
                await session.execute(stmt)
    except Exception as e:
        raise ErrorUpdateLikePost 
        

