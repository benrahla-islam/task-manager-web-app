from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey
from sqlalchemy.orm import validates
from flask_login import UserMixin

db = SQLAlchemy()

class User(db.Model , UserMixin):
    __tablename__ = 'user'
    id = db.Column("id",db.Integer , primary_key = True , autoincrement = True)
    email = db.Column("email", db.String(100), unique = True , nullable = False)
    username = db.Column("username", db.String(100), nullable = False)
    password = db.Column("password", db.String(100) , nullable = False)
    subscription_type = db.Column("subscription_type", db.Enum('basic','premium','admin') , default = 'basic')
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), 
                          onupdate=db.func.current_timestamp())

    def __init__(self , username , email , password ):
        self.username = username
        self.email = email
        self.password = password

    @validates('email')
    def validate_email(self, key , email):
        if not email or '@' not in email:
            raise ValueError("Invalid email address.")
        return email

    @validates('username')
    def validate_username(self, key  ,username):
        if not username:
            raise ValueError("Username cannot be empty.")
        return username

    @validates('password')
    def validate_password(self, key , password):
        if not password or len(password) < 8:
            raise ValueError("Password must be at least 8 characters long.")
        return password



class Task(db.Model):
    __tablename__ = 'task'
    id = db.Column("id",db.Integer , primary_key = True , autoincrement = True)
    title = db.Column("title", db.String(200) , nullable = False)
    description = db.Column("description", db.String(500), nullable = True)
    status = db.Column("status", db.Enum('active','inactive') , default = 'active')
    group_id = db.Column(db.Integer, ForeignKey('group.id'), nullable=True)
    user_id = db.Column(db.Integer , ForeignKey('user.id') , nullable = False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), 
                          onupdate=db.func.current_timestamp())

    group = db.relationship('Group', backref='tasks')
    user = db.relationship('User', backref='tasks')

    def __init__(self,title,user_id , description = None , group_id = None  , status = 'active'):
        self.title = title
        self.description = description
        self.group_id = group_id
        self.user_id = user_id
        self.status = status
        
    @validates('title')
    def validate_title(self, key , title):
        if not title:
            raise ValueError("Title cannot be empty.")
        return title


class Group(db.Model):
    __tablename__ = 'group'
    id = db.Column("id",db.Integer, primary_key = True , autoincrement = True)
    name = db.Column("name", db.String(50) , nullable = False)
    color = db.Column("color", db.String(10) , default = 'blue')
    user_id = db.Column(db.Integer , ForeignKey('user.id') , nullable = False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), 
                          onupdate=db.func.current_timestamp())

    user = db.relationship('User', backref='groups')

    def __init__(self,name,user_id , color = 'blue' ):
        self.name = name 
        self.color = color
        self.user_id = user_id
