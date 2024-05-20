from flask_bcrypt import Bcrypt
from .app import app
from .models import db, Category, Product, User, Order, OrderItem, Payment
from datetime import datetime


bcrypt = Bcrypt(app)

def seed_data():
    with app.app_context():
        # Create all tables
        db.create_all()

        # Delete existing data
        print('Deleting existing data...')
        Category.query.delete()
        Product.query.delete()
        User.query.delete()
        Order.query.delete()
        OrderItem.query.delete()
        Payment.query.delete()

        # Seed Users
        print('Creating user objects...')
        users = [
            User(username="Anna Kioko", email="anna@gmail.com", password=bcrypt.generate_password_hash("Annakioko.123").decode('utf-8'), role='admin', department='Sales'),
            User(username="Sharon Mwende", email="sharon@gmail.com", password=bcrypt.generate_password_hash("Sharonmwende.123").decode('utf-8'), role='admin', department='Product Manager'),
            User(username="James Mbuvi", email="james@gmail.com", password=bcrypt.generate_password_hash("Jamesmbuvi.123").decode('utf-8'), role='user', department='N/A'),
            User(username="Francis Ngigi", email="francis@gmail.com", password=bcrypt.generate_password_hash("francisngigi.123").decode('utf-8'), role='user', department='N/A'),
            User(username="Ian Kinuthia", email="ian@gmail.com", password=bcrypt.generate_password_hash("Iankinuthia.123").decode('utf-8'), role='user', department='N/A')
        ]

        print('Adding user objects to transaction...')
        db.session.add_all(users)
        db.session.commit()

        # Seed Categories
        print('Creating category objects...')
        category_makeup = Category(name='Makeup')
        category_fragrances = Category(name='Fragrances')
        category_skincare = Category(name='Skincare')

        print('Adding category objects to transaction...')
        db.session.add_all([category_makeup, category_fragrances, category_skincare])
        db.session.commit()

        # Seed Products
        print('Creating product objects...')
        products = [

            # Makeup products
            Product(name='soft matte lip colour', gender='Woman', description='Luxurious, velvety, long-lasting shades for irresistible lips', price=1000, quantity_available=50, image='https://unsplash.com/photos/beige-becca-lipstick-jaV6cvSEqao', category=category_makeup),
            Product(name='radiant silk', gender='Woman', description='Silky smooth formula for flawless coverage and luminous complexion', price=1500, quantity_available=40, image='https://unsplash.com/photos/two-labeled-bottles-xBqYLnRhfaI', category=category_makeup),
            Product(name='golden glow', gender='Woman', description='Illuminating formula for a radiant, dewy complexion all day', price=500, quantity_available=40, image='https://unsplash.com/photos/white-petaled-flowers-on-top-of-conceleaer-bzBs0_g0lRo', category=category_makeup),
            Product(name='flawless finish setting powder', gender='Woman', description='Translucent, lightweight setting powder for a matte finish and all-day wear', price=2500, quantity_available=10, image='https://unsplash.com/photos/a-small-jar-of-white-powder-on-a-wooden-tray-qOL9LA6iQAo', category=category_makeup),
            Product(name='High Shine Lipgloss', gender='Woman', description='Ultra-glossy, non-sticky formula for dazzling lips with a hint of color', price=500, quantity_available=40, image='https://unsplash.com/photos/a-close-up-of-a-flower-on-a-table-zDh4qX5L8dU', category=category_makeup),
            Product(name='lash lengthening mascara', gender='Woman', description='Intense black formula that lengthens and volumizes lashes for a dramatic look', price=500, quantity_available=20, image='https://unsplash.com/photos/white-petaled-flowers-on-top-of-conceleaer-bzBs0_g0lRo', category=category_makeup),
            

            # Fragrances products
            Product(name='enchanted elixir', gender='Woman', description='Enchanted Elixir: Captivating blend of florals and musk, evoking timeless elegance', price=4000.99, quantity_available=30, image='https://unsplash.com/photos/two-clear-glass-perfume-bottles-nka_sIQpKEU', category=category_fragrances),
            Product(name='midnight legend', gender='Man', description='Description for Product 4', price=4500, quantity_available=20, image='https://unsplash.com/photos/calvin-klein-one-perfume-bottle-C1qrJ9i4EPc', category=category_fragrances),
            Product(name='whispering petals', gender='Woman', description='Delicate floral notes intertwine for an enchanting, feminine aura', price=5000, quantity_available=20, image='https://unsplash.com/photos/pink-and-silver-perfume-bottle-M3PWXjCiRbQ', category=category_fragrances),
            Product(name='ocean breeze', gender='Man', description='Fresh and invigorating scent with notes of sea salt and citrus', price=4800, quantity_available=25, image='https://unsplash.com/photos/kind-dark-skinned-man-being-in-bathroom-while-demonstrating-his-favorite-perfume-preparing-for-the-date-TTd2Db6vnxY', category=category_fragrances),
            Product(name='velvet night', gender='Man', description='Luxurious blend of leather and spices for a sophisticated, masculine scent', price=4700, quantity_available=22, image='https://unsplash.com/photos/bleu-de-chanel-perfume-bottle-2b0JeJTEclQ', category=category_fragrances),
            Product(name='rose allure', gender='Woman', description='Exquisite blend of roses and jasmine, creating a captivating, feminine fragrance', price=5200, quantity_available=18, image='https://unsplash.com/photos/a-bottle-of-perfume-sitting-on-top-of-a-table-CrU1fVVYRB4', category=category_fragrances),
            
            # Skincare products
            Product(name='i am fabulous', gender='Woman', description='Luxurious body oil, enhances radiance, nourishes, and revitalizes skin', price=1500, quantity_available=10, image='https://unsplash.com/photos/brown-glass-bottle-beside-box-WnVrO-DvxcE', category=category_skincare),
            Product(name='necessarie', gender='Woman', description='Indulgent hydration, leaving skin supple, silky, and irresistibly smooth', price=1000, quantity_available=5, image='https://unsplash.com/photos/white-calvin-klein-soft-tube-p3O5f4u95Lo', category=category_skincare),
            Product(name='because its you', gender='Woman', description='Luxurious hydration, embracing your unique essence with confidence and grace', price='1500', quantity_available='30', image='https://unsplash.com/photos/white-calvin-klein-one-soft-tube-zot788TQRDU', category=category_skincare),
            Product(name='Revitalizing Face Cream', gender='Man', description='Hydrating face cream for men, designed to revitalize and protect the skin', price=2000, quantity_available=35, image='https://unsplash.com/photos/clarins-cream-soft-tube-7lFGxDph5KQ', category=category_skincare),
            Product(name='Men\'s Daily Moisturizer', gender='Man', description='Lightweight daily moisturizer for men, providing all-day hydration and comfort', price=1800, quantity_available=30, image='https://unsplash.com/photos/white-aveena-pump-bottle-DGlqrcZNtqM', category=category_skincare),
            Product(name='Men\'s Anti-Aging Serum', gender='Man', description='Powerful anti-aging serum for men, reducing wrinkles and improving skin elasticity', price=2500, quantity_available=25, image='https://unsplash.com/photos/white-plastic-container-07BEYT2hjGw', category=category_skincare)
        ]


        print('Adding product objects to transaction...')
        db.session.add_all(products)
        db.session.commit()

        # Seed Orders
        print('Creating order objects...')
        orders = [
            Order(timestamp=datetime.strptime('2023-01-01', '%Y-%m-%d'), total_amount=5000, payment_status='completed', shipping_address='123 Main St', payment_method='card', user_id=users[0].id),
            Order(timestamp=datetime.strptime('2023-02-01', '%Y-%m-%d'), total_amount=3000, payment_status='pending', shipping_address='456 Oak St', payment_method='mpesa', user_id=users[1].id),
            Order(timestamp=datetime.strptime('2023-03-01', '%Y-%m-%d'), total_amount=1500, payment_status='failed', shipping_address='789 Pine St', payment_method='card', user_id=users[2].id)
        ]

        print('Adding order objects to transaction...')
        db.session.add_all(orders)
        db.session.commit()

        # Seed OrderItems
        print('Creating order item objects...')
        order_items = [
            OrderItem(order_id=orders[0].id, product_id=products[0].id, quantity=2, price=products[0].price),
            OrderItem(order_id=orders[0].id, product_id=products[1].id, quantity=1, price=products[1].price),
            OrderItem(order_id=orders[1].id, product_id=products[2].id, quantity=3, price=products[2].price),
            OrderItem(order_id=orders[2].id, product_id=products[3].id, quantity=1, price=products[3].price)
        ]

        print('Adding order item objects to transaction...')
        db.session.add_all(order_items)
        db.session.commit()

        # Seed Payments
        print('Creating payment objects...')
        payments = [
            Payment(amount=5000, method='card', status='completed', order_id=orders[0].id),
            Payment(amount=3000, method='mpesa', status='pending', order_id=orders[1].id),
            Payment(amount=1500, method='card', status='failed', order_id=orders[2].id)
        ]

        print('Adding payment objects to transaction...')
        db.session.add_all(payments)
        db.session.commit()

        print('Complete.')

if __name__ == '__main__':

    seed_data()
