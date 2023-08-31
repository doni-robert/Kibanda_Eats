#!/usr/bin/python3
'''
Post Model
'''

from models.base_model import Base, BaseModel
from uuid import uuid4
from datetime import datetime
from sqlalchemy import Column, String, Integer, DateTime, func
from sqlalchemy import create_engine, ForeignKey, Sequence
from sqlalchemy.orm import relationship
from datetime import datetime


class Post(BaseModel, Base):
    '''Representation of post'''
    __tablename__ = 'posts'

    id = Column(Integer, Sequence('post_id_seq', start=1, increment=1),
                     primary_key=True)
    description = Column(String(256), nullable=False)
    location = Column(String(256), nullable=False)
    comment = Column(String(256), nullable=False)
    price = Column(Integer, nullable=False)
    image = Column(String(120), default='image.jpg')
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    def __init__(self, description, price, location, comment, image, user_id):
        ''' Initializes instance of the class '''
        self.description = description
        self.comment = comment
        self.price = price
        self.location = location
        self.image = image
        self.user_id = user_id
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()
