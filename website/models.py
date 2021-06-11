from . import db
from sqlalchemy import func
from flask_login import UserMixin

class Community(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    data = db.Column(db.String(1000))
    date = db.Column(db.DateTime(timezone=True),default = func.now())
    user_id = db.Column(db.Integer,db.ForeignKey('use.id'))

class Note(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    data = db.Column(db.String(1000))
    date = db.Column(db.DateTime(timezone=True),default = func.now())
    user_id = db.Column(db.Integer,db.ForeignKey('use.id'))

class Use(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key= True)
    email = db.Column(db.String(150),unique=True)
    password = db.Column(db.String(150))
    first_name =db.Column(db.String(150))
    notes = db.relationship('Note')
    Cnotes = db.relationship('Community')


