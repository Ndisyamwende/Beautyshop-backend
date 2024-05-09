from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import validates, relationship
from sqlalchemy.ext.associationproxy import association_proxy

db = SQLAlchemy()

# Define models

class User(db.Model, SerializerMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    role = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        return f"User('{self.email}', '{self.role}')"
pass




# # # Product model
# # class Product(db.Model):
# #     pass




# # # Order model
# # class Order(db.Model):
# #     pass



# # # Analytics model
# # class Order(db.Model):
# #     pass





# # Category model
# class Category(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(100), nullable=False, unique=True)
#     # Define relationship: a category can have many products
#     products = db.relationship('Product', backref='category', lazy=True)