from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Column, ForeignKey, Integer, Enum
from sqlalchemy.orm import Relationship

db = SQLAlchemy()


class User(db.Model):
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True)
    firstname = Column(String(50))
    lastname = Column(String(50))
    email = Column(String(50), unique=True)

    following = Relationship(
        "Follower", foreign_keys="[Follower.user_from_id]", back_populates="follower")
    followers = Relationship(
        "Follower", foreign_keys="[Follower.user_to_id]", back_populates="followed")
    comments = Relationship("Comment", back_populates="author")
    posts = Relationship("Post", back_populates="author")

    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            "firstname": self.firstname,
            "lastname": self.lastname,
            "email": self.email,
        }


class Follower(db.Model):
    user_from_id = Column(Integer, ForeignKey("User.id"))
    user_to_id = Column(Integer, ForeignKey("User.id"))

    follower = Relationship(
        "User", foreign_keys="[Follower.user_from_id]", back_populates="following")
    followed = Relationship(
        "User", foreign_keys="[Follower.user_to_id]", back_populates="followers")

    def serialize(self):
        return {
            "user_from_id": self.user_from_id,
            "user_to_id": self.user_to_id,
        }


class Comment(db.Model):
    id = Column(Integer, primary_key=True)
    comment_text = Column(String(200))
    author_id = Column(Integer, ForeignKey("User.id"))
    post_id = Column(Integer, ForeignKey("Post.id"))

    author = Relationship("User", back_populates="comments")
    post = Relationship("Post", back_populates="comments")

    def serialize(self):
        return {
            "id": self.id,
            "comment_text": self.comment_text,
            "author_id": self.author_id,
            "post_id": self.post_id,
        }


class Post(db.Model):
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("User.id"))

    author = Relationship("User", back_populates="posts")
    comments = Relationship("Comment", back_populates="posts")
    media = Relationship("Media", back_populates="posts")

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
        }


class Media(db.Model):
    id = Column(Integer, primary_key=True)
    type = Column(Enum("img"))
    url = Column(String(2048))
    post_id = Column(Integer, ForeignKey("Post.id"))

    post = Relationship("Post", back_populates="media")

    def serialize(self):
        return {
            "id": self.id,
            "type": self.type,
            "url": self.url,
            "post_id": self.post_id,
        }
