# -*- coding: utf-8 -*-
"""
Created on Wed May  4 13:04:51 2016

@author: Chirgal.Hansdah
"""

from flask import Flask
from flask.ext.mongoalchemy import MongoAlchemy

app = Flask(__name__)
app.config['MONGOALCHEMY_DATABASE'] = 'test-db'
db = MongoAlchemy(app)


class User(db.Document):
    firstname= db.StringField()
    lastname = db.StringField()
    email = db.StringField()
    password = db.StringField()
    catagories =db.ListField(db.StringField())

class Item(db.Document):
    catagory= db.StringField()
    details=db.StringField()
    amount=db.FloatField()


#class Expense(db.Document):
#    catagory= db.StringField()
#    details=db.StringField()
#    amount=db.FloatField()
#    date=db.DateTimeField()
#    user=db.StringField()

class Expense(db.Document):
    user=db.StringField()
    date=db.DateTimeField()
    items=db.ListField(db.DocumentField(Item))