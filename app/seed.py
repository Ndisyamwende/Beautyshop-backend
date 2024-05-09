
from app import app, db
from models import User, bcrypt

def seed_data():
    with app.app_context():
        
        db.create_all()

        
        hashed_password = bcrypt.generate_password_hash('password').decode('utf-8')
        admin_user = User(email='admin@example.com', password=hashed_password, role='admin')
        regular_user = User(email='user@example.com', password=hashed_password, role='user')

        db.session.add(admin_user)
        db.session.add(regular_user)

        db.session.commit()

if __name__ == "__main__":
    seed_data()


