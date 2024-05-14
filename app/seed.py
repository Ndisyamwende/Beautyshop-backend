# seed.py

from app import app, db
from models import User, Product, Order, Category, Contact
from flask_bcrypt import Bcrypt

    # seed.py

from app import app, db
from models import User, Product, Order, Category, Contact
from flask_bcrypt import Bcrypt,app
from models import Admin, Customer

def seed_database():
    bcrypt = Bcrypt()

    with app.app_context():
        db.create_all()

        # Create instances of Contact
        contacts = [
            Contact(name='John Doe', email='john@example.com', message='Hello, world!'),
            Contact(name='Jane Doe', email='jane@example.com', message='Nice to meet you!')
        ]
        db.session.add_all(contacts)
        db.session.commit()

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

    # Create sample orders
    order1 = Order(user_id=admin_user.id)
    order2 = Order(user_id=regular_user.id)

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
