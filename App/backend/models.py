from flask_sqlalchemy import SQLAlchemy
from App import app
import App.backend.settings
from datetime import datetime
import pytz

db = SQLAlchemy(app)


def timezone():
    d_naive = datetime.utcnow()
    timezone = pytz.timezone("Asia/Gaza")
    d_aware = timezone.localize(d_naive)
    return d_aware


class User(db.Model):
    id = db.Column(db.Integer, unique=True, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    username = db.Column(db.Integer, nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return '<id {}> <name {}> <username {}> <password {}>'.format(self.id,
                                                                      self.name,
                                                                      self.username,
                                                                      self.password)


class Admin(db.Model):
    id = db.Column(db.Integer, unique=True, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    username = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return '<id {}> <name {}> <username {}> <password {}>'.format(self.id,
                                                                      self.name,
                                                                      self.username,
                                                                      self.password)


class Rooms(db.Model):
    id = db.Column(db.Integer, unique=True, primary_key=True)
    name = db.Column(db.String(255))
    admin_id = db.Column(db.Integer, nullable=False)
    random_id = db.Column(db.String(255), nullable=False, unique=True)
    timeStart = db.Column(db.DateTime, nullable=False)
    timeFinished = db.Column(db.DateTime, nullable=False)

    def __repr__(self):
        return '<id {}> <admin_id {}> <random_id {}> <timeStart {}> <timeFinished {}>'.format(self.id,
                                                                                              self.admin_id,
                                                                                              self.random_id,
                                                                                              self.timeStart,
                                                                                              self.timeFinished)


class signIn(db.Model):
    id = db.Column(db.Integer, unique=True, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    room_id = db.Column(db.String(255), nullable=False)
    time_login = db.Column(db.DateTime, nullable=False, default=timezone())

    def __repr__(self):
        return '<id {}> <user_id {}> <rome_id {}> <time_login {}>'.format(self.id,
                                                                          self.user_id,
                                                                          self.room_id,
                                                                          self.time_login)
