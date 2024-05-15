from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import validates, relationship
from sqlalchemy.ext.associationproxy import association_proxy
import re
from sqlalchemy import CheckConstraint

db = SQLAlchemy()

#Define model
class User(db.Model, SerializerMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    role = db.Column(db.String(20), nullable=False)
    address = db.Column(db.String, nullable=True, default='N/A' )

        #relationship with order model
    orders = db.relationship('Order', back_populates='customer', lazy=True)

        # Define one-to-many relationship with Cart
    cart = db.relationship('Cart', back_populates='user', lazy=True)

    @validates('role')
    def validate_role(self, key, role):
        if role != 'user' and role != 'admin':
            raise ValueError("Invalid! User must be either user or admin.")
        return role

       
    # email
    @validates('email')
    def validate_email(self, key, email):
        assert '@' in email
        assert re.match(r"[^@]+@[^@]+\.[^@]+", email), "Invalid email format"
        return email
    
    # password
    @validates('password')
    def validate_password(self, key, password):
        assert len(password) > 8
        assert re.search(r"[A-Z]", password), "Password should contain at least one uppercase letter"
        assert re.search(r"[a-z]", password), "Password should contain at least one lowercase letter"
        assert re.search(r"[0-9]", password), "Password should contain at least one digit"
        assert re.search(r"[!@#$%^&*(),.?\":{}|<>]", password), "Password should contain at least one special character"
        return password

    def __repr__(self):
        return f"<User {self.id}, {self.username}, {self.email}, {self.password}, {self.role}, {self.address}>"


class Order(db.Model, SerializerMixin):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.Date, nullable=False)
    payment_status = db.Column(db.String(50), nullable=False)
    shipping_address = db.Column(db.String(255), nullable=True, default='N/A')
    payment_method = db.Column(db.String(50), nullable=False)
    total_cost = db.Column(db.Float, nullable=False, default=0)
    
        #relationship with user
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    customer = db.relationship('User', back_populates='orders')

     #relationship with orderitem
    order_product = db.relationship('OrderItem', back_populates='order', lazy=True)
      
      #relationship with payment model
    payment = db.relationship('Payment', back_populates='order', uselist=False)

    # def serialize(self):
    #     return {
    #         'id': self.id,
    #         'order_date': self.order_date.strftime('%Y-%m-%d %H:%M:%S'),
    #         'total_amount': self.total_amount,
    #         'payment_status': self.payment_status,
    #         'shipping_address': self.shipping_address,
    #         'payment_method': self.payment_method,
    #         'user_id': self.user_id
    #     }
    
    def __repr__(self):
        return f"<Order {self.id}, {self.order_date}, {self.total_amount}, {self.payment_status}, {self.shipping_address}, {self.payment_method}>"

    
class OrderProduct(db.Model, SerializerMixin):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    price = db.Column(db.Float, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)

        # relationships with Order and Product models
    order = db.relationship('Order', back_populates='order_product')
    product = db.relationship('Product', back_populates='order_product', lazy=True)
    cart_id = db.Column(db.Integer, db.ForeignKey('carts.id'), nullable=False)

        # Define relationship with Cart model
    cart = db.relationship('Cart', back_populates='order_product')

    # def serialize(self):
    #     return {
    #         'id': self.id,
    #         'order_id': self.order_id,
    #         'product_id': self.product_id,
    #         'quantity': self.quantity,
    #         'price': self.price
    #     }
    

    def __repr__(self):
        return f"<OrderItem {self.id}, {self.quantity}, {self.price}>"
    
class Product(db.Model, SerializerMixin):
    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    gender = db.Column(db.String, CheckConstraint("gender IN ('Male', 'Female')"))
    description = db.Column(db.String, nullable=False)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    quantity_available = db.Column(db.Integer)
    image = db.Column(db.String, nullable=True)

    # def serialize(self):
    #     return {
    #         'id': self.id,
    #         'name': self.name,
    #         'gender': self.gender,
    #         'description': self.description,
    #         'price': str(self.price),  
    #         'quantity_available': self.quantity_available,
    #         'image': self.image,
    #         'category': self.category.serialize() if self.category else None
    #     }
    

    # relationship with category 
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
    category = db.relationship('Category', back_populates='products_list')

    #relationship to order item 
    order_product = db.relationship('OrderItem', back_populates='product', lazy=True)

    #  relationship with ProductAnalytics model
    analytics = db.relationship('ProductAnalytics', back_populates='product')

    @validates('description')
    def validate_description(self, key, description):
        if not 5 <= len(description) <= 100:
           raise ValueError("Description must be between 5 and 100 characters.")
        return description
    
    def __repr__(self):
        return f"<Product {self.id}, {self.name}, {self.gender}, {self.category}, {self.description}, {self.price}>"
    
class Category(db.Model, SerializerMixin):
    _tablename_ = 'categories'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)

    # relationship with product
    products_list = db.relationship('Product', back_populates='category', lazy=True)

    # def serialize(self):
    #     return {
    #         'id': self.id,
    #         'name': self.name,
           
    #     }

    def _repr_(self):
        return f"<Category {self.id}, {self.name}>"
    
class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    message = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f"Contact(name={self.name}, email={self.email})"
    

#payment model
class Payment(db.Model):
    __tablename__ = 'payments'

    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Integer, nullable=False)
    method = db.Column(db.String, nullable=False)
    status = db.Column(db.String, nullable=False, default='pending')
  


    # Define relationship with Order model
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    order = db.relationship('Order', back_populates='payment')

    def serialize(self):
        return {
            'id': self.id,
            'amount': self.amount,
            'method': self.method,
            'status': self.status,
            'order_id': self.order_id
        }
    
    @validates(method)
    def validate_method(self, key, method):
        if method not in ['card', 'mpesa', 'cash_on_pickup']:
            raise ValueError("Invalid payment method.")
        return method


    @validates('status')
    def validate_status(self, key, status):
        if status not in ['pending', 'completed', 'failed']:
            raise ValueError("Invalid payment status.")
        return status

    def __repr__(self):
        return f"<Payment {self.id}, {self.amount}, {self.method}, {self.status}>"
