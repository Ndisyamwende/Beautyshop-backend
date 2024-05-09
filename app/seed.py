from app import db, User

def seed_database():
    
    
    user1 = User(email="james@gmail.com", password="example")
    user2 = User(email="james1@gmail.com", password="12345678909")
    user3 = User(email="example@gmail.com", password="example")


    db.session.add(user1)
    db.session.add(user2)
    db.session.add(user3)
    db.session.commit()

if __name__ == "__main__":
    
    seed_database()
    print("Database seeding completed.")
