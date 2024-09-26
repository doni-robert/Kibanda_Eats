#!/usr/bin/python3
'''
User Model
'''
import models
from models.base_model import Base, BaseModel
from models.post import Post
from uuid import uuid4
from datetime import datetime
import sqlalchemy
import bcrypt
from sqlalchemy import Column, String, Integer, DateTime, func
from sqlalchemy import create_engine, Boolean, ForeignKey, Sequence
from sqlalchemy.orm import relationship, sessionmaker
from flask_login import UserMixin


class User(UserMixin, BaseModel, Base):
    ''' Representation of user '''
    __tablename__ = 'users'

    id = Column(Integer, Sequence('user_id_seq', start=1, increment=1),
                primary_key=True)
    password = Column(String(100), nullable=False)
    username = Column(String(100), nullable=False, unique=True)
    email = Column(String(256), nullable=False, unique=True)
    posts = relationship("Post", backref="user")
    
    def __init__(self, password, username, email):
        ''' initializes an instance of the model '''
        self.password = self.set_password(password)
        self.username = username
        self.email = email

    def set_password(self, password):
        ''' hashes password '''
        pwd_bytes = password.encode('utf-8')
        hashed_pwd = bcrypt.hashpw(pwd_bytes, bcrypt.gensalt())
        return hashed_pwd.decode('utf-8')

    def check_password(self, password):
        ''' checks password '''
        pwd_bytes = password.encode('utf-8')
        hashed_password = self.password
        return bcrypt.checkpw(pwd_bytes, hashed_password.encode('utf-8'))
    
    def get_id(self):
        ''' Returns the user ID as a string '''
        return str(models.storage.getUserObj(User, self.email).to_dict()['id'])

    @property
    def is_authenticated(self):
        ''' Returns True if the user is authenticated '''
        return True

    @property
    def is_active(self):
        ''' Returns True if the user is active '''
        return True
