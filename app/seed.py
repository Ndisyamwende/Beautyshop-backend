from app.app import app, db
from app.models import User, Product, Order, Category, Contact
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)

from models import db, User, Order, OrderProduct, Product, Category, Contact, Payment

# Create users
users_data = [
    {'username': 'john_doe', 'email': 'john@example.com', 'password': 'password123', 'role': 'user', 'address': '123 Main St'},
    {'username': 'jane_smith', 'email': 'jane@example.com', 'password': 'password456', 'role': 'user', 'address': '456 Elm St'},
    {'username': 'admin', 'email': 'admin@example.com', 'password': 'admin123', 'role': 'admin', 'address': '789 Oak St'}
]

for user_data in users_data:
    user = User(**user_data)
    db.session.add(user)

# Create categories
categories_data = [
    {'name': 'Skincare'},
    {'name': 'Makeup'},
    {'name': 'Scents'}
]

for category_data in categories_data:
    category = Category(**category_data)
    db.session.add(category)

# Create products
products_data = [
    {'name': 'Moisturizer', 'gender': 'Female', 'description': 'Hydrates the skin', 'price': 20.00, 'quantity_available': 100, 'category_id': 1},
    {'name': 'Lipstick', 'gender': 'Female', 'description': 'Adds color to lips', 'price': 15.00, 'quantity_available': 50, 'category_id': 2},
    {'name': 'Crede Aventus', 'gender': 'Male', 'description': 'Fruity scent', 'price': 10.00, 'quantity_available': 75, 'category_id': 3}
]

for product_data in products_data:
    product = Product(**product_data)
    db.session.add(product)

# Commit changes to the database
db.session.commit()

print("Data seeded successfully!")
