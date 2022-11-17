import requests

STATUS_CODE_OK = 200
STATUS_CODE_CONFLICT  = 409
STATUS_CODE_FORBIDDEN = 403
STATUS_CODE_BAD_REQUEST = 400
STATUS_CODE_CREATED = 201
STATUS_CODE_UNATHORIZED = 401

#### login ####
#Note : real username and passwword - eli: username , password: password
#correct login entrance
def test_login_status_200():
        login = requests.post("http://localhost:8000/login" , json = {"username" : "eli", "password" : "password"})
        assert login.status_code == STATUS_CODE_OK
#wrong json user not exist 
def test_login_status_409():
        login = requests.post("http://localhost:8000/login" , json = {"username" : "blaeraf", "password" : "passwod"})
        assert login.status_code == STATUS_CODE_CONFLICT
#wrong password
def test_login_status_403():
        login = requests.post("http://localhost:8000/login" , json = {"username" : "eli", "password" : "1234567"})
        assert login.status_code == STATUS_CODE_FORBIDDEN
#wrong json
def test_login_status_400():
        login = requests.post("http://localhost:8000/login" , json = {"u" : "ei", "password" : "password"})
        assert login.status_code == STATUS_CODE_BAD_REQUEST

#### sign-up ####
#Note  : user and pass need to be more than 3 char plus user contain letter,number,_,- only
#correct sign-up
def test_sign_up_201(username, password):
    sign_up = requests.put("http://localhost:8000/create-user" , json = {"username" : username ,  "password" : password})
    assert sign_up.status_code == STATUS_CODE_CREATED
#username exist 
def test_sign_up_409():
    sign_up = requests.put("http://localhost:8000/create-user" , json = {"username" : "eii", "password" : "passqweword"})
    assert sign_up.status_code == STATUS_CODE_CONFLICT
#wrong json
def test_sign_up_400():
    sign_up = requests.put("http://localhost:8000/create-user" , json = {"u" : "ei", "password" : "password"})
    assert sign_up.status_code == STATUS_CODE_BAD_REQUEST

#### blog ####

#get all blogs
#correct get all 
def test_get_all_blogs_200():
    blogs = requests.get("http://localhost:8000/blogs")
    assert blogs.status_code == STATUS_CODE_OK

#not exists posts
def test_get_all_blogs_409():
    blogs = requests.get("http://localhost:8000/blogs")
    assert blogs.status_code == STATUS_CODE_CONFLICT

#get post by id
#correct blog (id blog 11 exist)
def test_get_blog_200():
    blog = requests.get("http://localhost:8000/blogs/blog/11")
    assert blog.status_code == STATUS_CODE_OK

#not exists posts
def test_get_blog_409():
    blog = requests.get("http://localhost:8000/blogs/98123")
    assert blog.status_code == STATUS_CODE_CONFLICT

#likd/dislike
#correct blog (id blog 11 exist)
#enter correct token by login 
def test_put_like_200(token):
    like = requests.put("http://localhost:8000/blogs/8/like" , headers={'x-access-token': token} ,json={"is_like" : True})
    assert like.status_code == STATUS_CODE_OK
# wrong token
def test_put_like_401():
    token = 'yJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjo2LCJleHAiOjE2NjgzODAxNDR9.faIn68r8E1aITbSTHda2KPBvScKCpJnZTx0vlEPiqcw'
    like = requests.put("http://localhost:8000/blogs/8/like" , headers={'x-access-token': token} ,json={"is_like" : True})
    assert like.status_code == STATUS_CODE_UNATHORIZED
#wrong json
def test_put_like_400():
    token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjo2LCJleHAiOjE2NjgzODAxNDR9.faIn68r8E1aITbSTHda2KPBvScKCpJnZTx0vlEPiqcw'
    like = requests.put("http://localhost:8000/blogs/8/like" , headers={'x-access-token': token} ,json={"isike" : True})
    assert like.status_code == STATUS_CODE_BAD_REQUEST

#add post
#correct add post 
def test_add_post_201(token):
    post = requests.put("http://localhost:8000/blogs/add-post", headers={'x-access-token': token} ,json={"title" : "asdasdsadasd" , "content" : "asdsad1123ad"})
    assert post.status_code == STATUS_CODE_CREATED
#wrong token
def test_add_post_401():
    token = 'yJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjo2LCJleHAiOjE2NjgzODAxNDR9.faIn68r8E1aITbSTHda2KPBvScKCpJnZTx0vlEPiqcw'
    post = requests.put("http://localhost:8000/blogs/add-post", headers={'x-access-token': token} ,json={"title" : "asdasdsadasd" , "content" : "asdsad1123ad"})
    assert post.status_code == STATUS_CODE_UNATHORIZED

def test_add_post_400(token):
    #wrong json
    post = requests.put("http://localhost:8000/blogs/add-post", headers={'x-access-token': token} ,json={"tite" : "asdasdsadasd" , "content" : "asdsad1123ad"})
    assert post.status_code == STATUS_CODE_BAD_REQUEST
    #check function content less then 1000 char's
    data = 'a' * 1111
    post = requests.put("http://localhost:8000/blogs/add-post", headers={'x-access-token': token} ,json={"title" : "qwenas" , "content" : data})
    assert post.status_code == STATUS_CODE_BAD_REQUEST
    #check function content as trailung space
    post = requests.put("http://localhost:8000/blogs/add-post", headers={'x-access-token': token} ,json={"title" : "asdasdsadasd" , "content" : "asds  ad"})
    assert post.status_code == STATUS_CODE_BAD_REQUEST
