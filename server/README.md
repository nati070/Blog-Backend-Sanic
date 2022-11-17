# Dcoya-Blog

# instructions: #
 * download/pull the files
 * add .env file (send in private)
   1) run with docker
     * create-img - docker build -t dcoya-image .
     * create & runcontainer - docker run --name mysanic -p 8000:8000 -d dcoya-image
   2) run with venv 
     * direct to ./env/Script/activate 
     * install requirements - py -m pip install -r requirements.txt 
     * run - python -m sanic server.app 
  
 ## explain about the dependencies ##
 - sanic - used with sanic for high performence with async
 - sqlalchemy - ORM for sql database 
 - aiomysql - for async req&res from db
 - pyJWT - token security for users
 - bcrpt - encrypt the passwords
 - python-decouple - store parameters in .env file
 - jsonschema - to validate json(for input json req)
 - sanic-openapi - for api documation Swagger 
 - requests - for create req to server(used for tests)
 
 ## explain about the routes ##
  1. login:
      -login req
  2. sign-up:
    -create-user req
  3. blogs:
      * all
        - get_all_blogs req - return all the exist blogs
        - get_post req - return specifi post by id 
      * users only
        - put_like - like/dislike of blog
        - put_add_post - create post
        - put_delete_post - delete post
        - put_edit_post - edit post 
 
 ## db sturcture ##
 * users - id: int:pk , username: str , password - str
 * posts - id: int:pk , authorId: int:fk , tite: str , password - str
 * likes - id: int:pk , userId: int:fk , postId: int:fk , islLike - bool
![alt text](/diagram.png)
    
    

      
 
 
 
 

 
