from flask_bcrypt import Bcrypt
from app import app
from models import db, Category, Product

bcrypt = Bcrypt(app)

def seed_data():
    # Delete existing data
    Category.query.delete()
    Product.query.delete()

if __name__ == '__main__':
    with app.app_context():
        seed_data()
