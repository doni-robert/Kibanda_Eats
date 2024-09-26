#!/usr/bin/python3
'''
Base Model
'''
import models
from uuid import uuid4
from datetime import datetime
import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class BaseModel():
    ''' Representation of basemodel '''

    def __init__(self):
        ''' initializes an instance of the model '''

    def __str__(self):
        ''' returns a string representation of an object '''
        return '[{}] ({}) {}'.format(type(self).__name__, self.id,
                                     self.__dict__)

    def save(self):
        ''' updates the attribute "updated_at" with the current time '''
        self.updated_at = datetime.utcnow()
        models.storage.new(self)
        models.storage.save()

    def to_dict(self):
        ''' returns a dictionary containing all key-value pair of the obj '''
        objs = self.__dict__.copy()
        objs['__class__'] = self.__class__.__name__
        if 'created_at' in objs.keys() and 'updated_at' in objs.keys():
            objs['created_at'] = objs['created_at'].isoformat()
            objs['updated_at'] = objs['updated_at'].isoformat()
        if '_sa_instance_state' in objs:
            del objs['_sa_instance_state']
        return objs
