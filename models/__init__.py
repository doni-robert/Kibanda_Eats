#!/usr/bin/python3
'''
Creates a storage instance
'''
from models.engine.storage import Storage
from models.user import User


storage = Storage()
storage.reload()
