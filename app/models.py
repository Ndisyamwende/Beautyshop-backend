from flask_sqlalchemy import SQLAlchemy
from uuid import uuid4
db = SQLAlchemy()



class User(db.Model):
  __tablename__ = "users"
  id = db.Column( db.Integer, primary_key=True )
  email = db.Column( db.String, unique = True ) 
  password = db.Column(db.String(30))