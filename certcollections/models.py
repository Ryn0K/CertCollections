from flask_login import UserMixin
from flask import current_app
from . import db


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    username = db.Column(db.String(1000))
    password = db.Column(db.String(100))
    admin = db.Column(db.Boolean(), default=False)
    avatar = db.Column(db.String(1000),default='defaultuser.png')

class Reportissue(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100))
    name = db.Column(db.String(1000))
    issue = db.Column(db.Text)
    status = db.Column(db.Boolean(), default=False)

class Upldoc(UserMixin,db.Model):
    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(100))
    description = db.Column(db.Text)
    doctype = db.Column(db.Text)
    location= db.Column(db.String(1000))
    userid = db.Column(db.Integer)
    private = db.Column(db.Boolean(),default=False)


