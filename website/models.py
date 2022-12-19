from . import db  #import from __init__
from flask_login import UserMixin
from sqlalchemy.sql import func

#need UserMixin to use current_user in auth.py

#create database
#one to many relationship

class Note(db.Model):
    #by default, don't need to add the id yourself, the db does it for you
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    #default=func.now() -> stores the current date time
    #let db handle the date format
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    #its an integer; foriegn key is the user table id
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

# in py, classes must be Uppercase so User but for db its lowercase
# so in ForeignKey, use user 
# class User would represent a user table in a db
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    #unique=True -> so only cant have same existing registered email
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    #everytime a new note is made, add a new note id to user
    #by using relationship, lets user have access to all their notes
    #for relationship, Uppercase
    notes = db.relationship('Note')
