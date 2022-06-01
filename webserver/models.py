from email.policy import default
from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class Note(db.Model): # Not Used
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(128))
    data = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class User(db.Model, UserMixin): # Used to verify login, maybe store pref.
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), unique=True)
    password = db.Column(db.String(32))
    notes = db.relationship('Note')
