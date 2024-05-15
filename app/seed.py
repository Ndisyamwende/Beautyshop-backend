from flask_bcrypt import Bcrypt
from app import app
from models import db, Category, Product, User, Order, OrderItem


bcrypt = Bcrypt(app)

def seed_data():
    # Delete existing data
    # Category.query.delete()
    # Product.query.delete()
    # User.query.delete()
    # Order.query.delete()
    # OrderItem.query.delete()

    # user seed
    Users = [
            User(username="Anna Kioko", email="anna@gmail.com", password=bcrypt.generate_password_hash("Annakioko.123").decode('utf-8'),  role='admin', department='Sales'),
            User(username="Sharon Mwende", email="sharon@gmail.com", password=bcrypt.generate_password_hash("Sharonmwende.123").decode('utf-8'),  role='admin', department='Product Manager'),
            User(username="James Mbuvi", email="james@gmail.com", password=bcrypt.generate_password_hash("Jamesmbuvi.123").decode('utf-8'),  role='user', department='N/A'),
            User(username="Francis Ngigi", email="francis@gmail.com", password=bcrypt.generate_password_hash("francisngigi.123").decode('utf-8'),  role='user', department='N/A'),
            User(username="Ian Kinuthia", email="ian@gmail.com", password=bcrypt.generate_password_hash("Iankinuthia.123").decode('utf-8'),  role='user', department='N/A')
        ]
    db.session.add_all(Users)
    db.session.commit()    
        



    #  categories seed
    category_makeup = Category(name='Makeup')
    category_Fragrances = Category(name='Fragrances')
    category_skincare = Category(name='Skincare')
    category_haircare = Category(name='Haircare')
    category_bathandbody = Category(name='Bathandbody')
    category_giftssetsandkits = Category(name='Giftssetsandkits')

    # Add categories to session
    db.session.add_all([category_makeup, category_Fragrances, category_skincare, category_haircare, category_bathandbody, category_giftssetsandkits])
    db.session.commit()

    # Create products
    products = [
        # Makeup products
        Product(name='soft matte lip colour', gender='Woman', description=' Luxurious, velvety, long-lasting shades for irresistible lips', price=1000, quantity_available=50, image='https://unsplash.com/photos/beige-becca-lipstick-jaV6cvSEqao', category=category_makeup),
        Product(name='radiant silk', gender='Woman', description='Silky smooth formula for flawless coverage and luminous complexion', price=1500, quantity_available=40, image='https://unsplash.com/photos/two-labeled-bottles-xBqYLnRhfaI', category=category_makeup),
        Product(name='golden glow', gender='Woman', description='Illuminating formula for a radiant, dewy complexion all day', price=500, quantity_available=40, image='https://unsplash.com/photos/white-petaled-flowers-on-top-of-conceleaer-bzBs0_g0lRo', category=category_makeup),

        # Fragrances products
        Product(name='enchanted elixir', gender='Woman', description='Enchanted Elixir: Captivating blend of florals and musk, evoking timeless elegance', price=4000.99, quantity_available=30, image='https://unsplash.com/photos/two-clear-glass-perfume-bottles-nka_sIQpKEU', category=category_Fragrances),
        Product(name='midnight legend', gender='Man', description='Description for Product 4', price=4500, quantity_available=20, image='https://unsplash.com/photos/calvin-klein-one-perfume-bottle-C1qrJ9i4EPc', category=category_Fragrances),
        Product(name='whispering petals', gender='Woman', description='Delicate floral notes intertwine for an enchanting, feminine aura', price=5000, quantity_available=20, image='https://unsplash.com/photos/pink-and-silver-perfume-bottle-M3PWXjCiRbQ', category=category_Fragrances),

        # Skincare products
        Product(name='i am fabulous', gender='Woman', description='Luxurious body oil, enhances radiance, nourishes, and revitalizes skin', price=1500, quantity_available=10, image='https://unsplash.com/photos/brown-glass-bottle-beside-box-WnVrO-DvxcE', category=category_skincare),
        Product(name='necessarie', gender='Woman', description='Indulgent hydration, leaving skin supple, silky, and irresistibly smooth', price=1000, quantity_available=5, image='https://unsplash.com/photos/white-calvin-klein-soft-tube-p3O5f4u95Lo', category=category_skincare),
        Product(name='because its you', gender='Woman', description='Luxurious hydration, embracing your unique essence with confidence and grace', price='1500', quantity_available='30', image='https://unsplash.com/photos/white-calvin-klein-one-soft-tube-zot788TQRDU', category=category_skincare)
    ]

    # Add products to session
    db.session.add_all(products)
    db.session.commit()




if __name__ == '__main__':
    with app.app_context():
        seed_data()








