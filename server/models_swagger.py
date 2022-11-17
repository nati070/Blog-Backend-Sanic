class Blog:
    id = int
    author_id = int
    title = str
    content = str("string max 5000")

class PostBlog:
    title = str
    content = str("string max 5000")

class Like:
    is_like = bool

class Login:
    username = str("string min 3 len without space")
    password = str("string min 3 len")