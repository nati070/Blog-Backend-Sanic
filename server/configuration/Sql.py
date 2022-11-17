from sqlalchemy.ext.asyncio import create_async_engine
from contextvars import ContextVar
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker

class SQLConfigre:
    
    def __init__(self,app,sql_uri):
        self._app = app
        self._bind = create_async_engine(sql_uri,echo=False) ##echo remove logger
        self._base_model_session_ctx = ContextVar("session")


    async def before_session(self,request):
        request.ctx.session = sessionmaker(self._bind,AsyncSession,expire_on_commit=False)()
        request.ctx.session_ctx_token = self._base_model_session_ctx.set(request.ctx.session)
    
    async def after_session(self,request):
        if hasattr(request.ctx, "session_ctx_token"):
            self._base_model_session_ctx.reset(request.ctx.session_ctx_token)
            await request.ctx.session.close()

    