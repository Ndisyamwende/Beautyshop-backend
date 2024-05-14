

    # seed.py

from app import db
from models import User, Product, Order, Category
from flask_bcrypt import Bcrypt,app
from models import Admin, Customer

# Function to seed the database with initial data
def seed_database():
    bcrypt = Bcrypt()
    # Create sample users
    hashed_password = bcrypt.generate_password_hash('password').decode('utf-8')
    admin_user = User(email='admin@example.com', password=hashed_password, role='admin')
    
    regular_user = User(email='user@example.com', password=hashed_password, role='user')

    # Create sample categories
    category1 = Category(name='Skin Care')
    category2 = Category(name='Scents')
    category3 = Category(name='Makeup')

    # Add sample users and categories to the database
    db.session.add(admin_user)
    db.session.add(regular_user)
    db.session.add(category1)
    db.session.add(category2)
    db.session.add(category3)
    db.session.commit()

    # Create sample products
    product1 = Product(name='Lipstick', description='Red lipstick for bold lips', price=10.99, stock=100, category_id=3)
    product2 = Product(name='Moisturizer', description='Hydrating moisturizer for smooth skin', price=19.99, stock=50, category_id=1)

    # Add sample products to the database
    db.session.add(product1)
    db.session.add(product2)
    db.session.commit()

    # Create sample orders (assuming user1 and user2 are instances of User model)
    user1 = User.query.filter_by(email='admin@example.com').first()
    user2 = User.query.filter_by(email='user@example.com').first()
    order1 = Order(user_id=user1.id)
    order2 = Order(user_id=user2.id)

    # Add sample orders to the database
    db.session.add(order1)
    db.session.add(order2)
    db.session.commit()


    # Seed Admins
    hashed_password = bcrypt.generate_password_hash('adminpassword').decode('utf-8')
    admin1 = Admin(username='admin1', password=hashed_password, role='admin')
    admin2 = Admin(username='admin2', password=hashed_password, role='admin')
    db.session.add(admin1)
    db.session.add(admin2)

    # Seed Customers
    hashed_password = bcrypt.generate_password_hash('customerpassword').decode('utf-8')
    customer1 = Customer(username='customer1', password=hashed_password, role='customer')
    customer2 = Customer(username='customer2', password=hashed_password, role='customer')
    db.session.add(customer1)
    db.session.add(customer2)

    db.session.commit()


if __name__ == '__main__':
    seed_database()


