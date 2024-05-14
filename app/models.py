from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import validates, relationship
from sqlalchemy.ext.associationproxy import association_proxy
import re
from sqlalchemy import CheckConstraint

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
    

class ProductAnalytics(db.Model, SerializerMixin):
    _tablename_ = 'product_analytics'

    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    total_sales = db.Column(db.Integer, nullable=False, default=0)

    
    # Define relationship with Product model
    product = db.relationship('Product', back_populates='analytics')

    def serialize(self):
        return {
            'id': self.id,
            'product_id': self.product_id,
            'total_sales': self.total_sales
        }

    def _repr_(self):
        return f"<PrductAnalytics{self.id}, {self.product_id}, {self.total_sales}>"

    

class ProductAnalytics(db.Model, SerializerMixin):
    _tablename_ = 'product_analytics'

    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    total_sales = db.Column(db.Integer, nullable=False, default=0)

    
    # Define relationship with Product model
    product = db.relationship('Product', back_populates='analytics')

    def serialize(self):
        return {
            'id': self.id,
            'product_id': self.product_id,
            'total_sales': self.total_sales
        }

    def _repr_(self):
        return f"<PrductAnalytics{self.id}, {self.product_id}, {self.total_sales}>"