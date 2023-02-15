"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)

class Post(db.Model):
    __tablename__ = 'posts'

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    title = db.Column(db.String(30), nullable=False)
    content = db.Column(db.String(280), nullable=False)
    created_at = db.Column(db.String) 
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

class User(db.Model):
    __tablename__ = 'users'

    def __repr__(self):
        u = self
        return f"<User id = {u.id}, username = {u.username},  first_name = {u.first_name}, last_name = {u.last_name}, image_url = {u.image_url}"

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    username = db.Column(db.String(30), nullable=False, unique=True)
    first_name = db.Column(db.String(15), nullable=False)
    last_name = db.Column(db.String(15), nullable=False)
    image_url = db.Column(db.String(500), nullable=True)
    posts = db.relationship('Post', backref='user',foreign_keys=[Post.user_id])


    
    
