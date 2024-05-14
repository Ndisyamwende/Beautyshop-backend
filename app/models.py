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
    
    

class Product(db.Model, SerializerMixin):
    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    gender = db.Column(db.String, CheckConstraint("gender IN ('Male', 'Female')"))
    description = db.Column(db.String, nullable=False)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    quantity_available = db.Column(db.Integer)
    image = db.Column(db.String, nullable=True)

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'gender': self.gender,
            'description': self.description,
            'price': str(self.price),  
            'quantity_available': self.quantity_available,
            'image': self.image,
            'category': self.category.serialize() if self.category else None
        }
    

    # relationship with category 
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
    category = db.relationship('Category', back_populates='products_list')

    #relationship to order item 
    order_items = db.relationship('OrderItem', back_populates='product', lazy=True)

    #  relationship with ProductAnalytics model
    analytics = db.relationship('ProductAnalytics', back_populates='product')

    @validates('description')
    def validate_description(self, key, description):
        if not 5 <= len(description) <= 100:
           raise ValueError("Description must be between 5 and 100 characters.")
        return description
    
    def __repr__(self):
        return f"<Product {self.id}, {self.name}, {self.gender}, {self.category}, {self.description}, {self.price}>"

    

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