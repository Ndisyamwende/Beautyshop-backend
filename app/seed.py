# seed.py

from app import db
from models import User, Product, Order, Category

# Function to seed the database with initial data
def seed_database():
    # Create sample users
    user1 = User(username='john_doe', email='john@example.com', password='password123')
    user2 = User(username='jane_smith', email='jane@example.com', password='password456')

    # Create sample categories
    category1 = Category(name='Skin Care')
    category2 = Category(name='Scents')
    category3 = Category(name='Makeup')

    # Add sample users and categories to the database
    db.session.add(user1)
    db.session.add(user2)
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

    # Create sample orders
    order1 = Order(user_id=user1.id)
    order2 = Order(user_id=user2.id)

    # Add sample orders to the database
    db.session.add(order1)
    db.session.add(order2)
    db.session.commit()

    # You can add more sample data as needed

if __name__ == '__main__':
    seed_database()
