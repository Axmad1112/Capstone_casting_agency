from flask_sqlalchemy import SQLAlchemy
from config import database_param
from datetime import date
import json
import os
from os import getenv


# database_path = "{}://{}:{}@localhost: 5432/{}".format(
#     database_param["dialect"],
#     database_param["username"],
#     database_param["password"],
#     database_param["db_name"])

database_path = getenv("DATABASE_URI")
db = SQLAlchemy()


def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    return db


def db_drop_and_create_all():
    db.drop_all()
    db.create_all()


class Actor(db.Model):
    __tablename__ = 'actors'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(), nullable=False)
    age = db.Column(db.Integer(), nullable=False)
    gender = db.Column(db.String(), nullable=False)
    movie_id = db.Column(db.Integer, db.ForeignKey('movies.id'), nullable=True)

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def get_format_json(self):
        return({
            "id": self.id,
            "name": self.name,
            "age": self.age,
            "gender": self.gender,
            'movie_id': self.movie_id
        })

    def __repr__(self):
        return f'Actor: {self.id}, {self.name}'


class Movie(db.Model):
    __tablename__ = 'movies'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String())
    release_date = db.Column(db.Date)
    actors = db.relationship('Actor', backref='movies')

    def __init__(self, title, release_date):
        self.title = title
        self.release_date = release_date

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'title': self.title,
            'release_date': self.release_date,
            'actors': [actor.name for actor in self.actors]}
