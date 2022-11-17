from sanic import Sanic 
from sanic_openapi import openapi3_blueprint

from config import DB_HOST,DB_NAME,DB_PASS
from configuration.Sql import SQLConfigre

from routes.blogs import bp as blogs_bp
from routes.login import bp as login_bp
from routes.sign_up import bp as sign_up_bp

app = Sanic('dcoyaBlog')

## swaggers configuration
app.config.API_TITLE = "Dcoya Blog-OpenAPI"
app.config.API_DESCRIPTION = "blog api documentation"

#sql configuration 
sql_url = f'mysql+aiomysql://{DB_NAME}:{DB_PASS}@{DB_HOST}'
sql_config = SQLConfigre(app , sql_uri= sql_url)

@app.middleware("request")
async def inject_session(request):
    await sql_config.before_session(request)

@app.middleware("response")
async def close_session(request, response):
    await sql_config.after_session(request)
    
app.blueprint(openapi3_blueprint)

app.blueprint(login_bp)

app.blueprint(sign_up_bp)

app.blueprint(blogs_bp)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)


#  for develop commend
#  python -m sanic --dev server.app 