
use dcoya;
CREATE TABLE users(
    id INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
    username varchar(100) NOT NULL, 
    `password` varchar(100) NOT NULL
);
CREATE TABLE blogs(
    id INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
    authorId INT,
    title varchar(100) NOT NULL,
    content varchar(5000) NOT NULL,
    FOREIGN KEY (authorId) REFERENCES users(id)
);
CREATE TABLE likes(
    id INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
    userId INT NOT NULL,
    blogId INT NOT NULL,
    isLike BIT NOT NULL,
    FOREIGN KEY(userId) REFERENCES users(id),
    FOREIGN KEY(blogId)  REFERENCES blogs(id)
);




