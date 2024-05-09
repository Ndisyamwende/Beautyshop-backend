from flask import Flask, request, jsonify, session
from flask_bcrypt import Bcrypt
from flask_session import Session
from config import ApplicationConfig
from flask_cors import CORS
from models import User,db

app = Flask(__name__)
CORS(app, supports_credentials=True)
bcrypt = Bcrypt(app)

@app.route("/signup", methods=["POST"])
def register_user():
    email = request.json["email"]
    password = request.json["password"]


    user_exists = User.query.filter_by(email=email).first() is not None

    if user_exists:
    
     return jsonify({"error": f"User with email {email} already exists"}), 409

    hashed_password = bcrypt.generate_password_hash(password)
    new_user = User(email=email, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()
    
    session["user_id"] = new_user.id
    return jsonify({
        "id": new_user.id,
        "email": new_user.email
    })

@app.route("/login", methods=["POST"])
def login_user():
    email = request.json["email"]
    password = request.json["password"]

    user = User.query.filter_by(email=email).first()

    if user is None:
        return jsonify({"error": "wrong email"}), 401
    if not bcrypt.check_password_hash(user.password, password):
        return jsonify({"error": "Password is incorrect"}), 401
    
    session["user_id"] = user.id
    return jsonify({
        "id": user.id,
        "email": user.email
    })

@app.route("/logout", methods=["POST"])
def logout_user():
    session.pop("user_id")
    return "200"

app.config.from_object(ApplicationConfig)
db.init_app(app)
with app.app_context():
  db.create_all()

  



  if __name__ == '__main__':
    app.run(port=5555, debug=True)