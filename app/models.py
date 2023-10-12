from flask_pymongo import PyMongo
class User:
    def __init__(self, name, username, password):
        self.name = name
        self.username = username
        self.password = password