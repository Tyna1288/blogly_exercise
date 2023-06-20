
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

DEFAULT_IMAGE_URL = "https://www.freeiconspng.com/uploads/icon-user-blue-symbol-people-person-generic--public-domain--21.png"


def connect_db(app):
   """Connect this db to provided Flask app"""
   db.app = app
   db.init_app(app)


"""Models for Blogly."""


class User(db.Model):
   __tablename__ = 'users'

   def _repr_(self):
      u = self
      return f"<user id=(u.id) first_name=(u.firstname) last_name=(u.lastname) image_url=(u.imageurl)>"

   id = db.Column(db.Integer,
                  primary_key=True,
                  autoincrement=True)

   first_name = db.Column(db.Text,
                          nullable=False,
                          unique=True)

   last_name = db.Column(db.Text,
                         nullable=False,
                         unique=True)

   image_url = db.Column(db.Text, nullable=False, default=DEFAULT_IMAGE_URL)
