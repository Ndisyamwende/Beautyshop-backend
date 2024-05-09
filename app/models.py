from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import validates, relationship
from sqlalchemy.ext.associationproxy import association_proxy
import re

db = SQLAlchemy()

# Define models

# User model
class User(db.Model):
    pass



# Product model
class Product(db.Model):
    pass




# Order model
class Order(db.Model):
    pass




# Category model
class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    # Define relationship: a category can have many products
    products = db.relationship('Product', backref='category', lazy=True)