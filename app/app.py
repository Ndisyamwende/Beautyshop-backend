from flask import Flask, request, jsonify
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from config import ApplicationConfig
from flask_cors import CORS
from models import User, db

app = Flask(__name__)
CORS(app, supports_credentials=True)
bcrypt = Bcrypt(app)
app.config.from_object(ApplicationConfig)
app.config['JWT_SECRET_KEY'] = 'ce2f33f294'
jwt = JWTManager(app)
db.init_app(app)

# Specific password for admin signup
ADMIN_SIGNUP_PASSWORD = "0000"

@app.route("/signup", methods=["POST"])
def register_user():
    email = request.json["email"]
    password = request.json["password"]
    role = request.json.get("role", "user")

    user_exists = User.query.filter_by(email=email).first() is not None

    if user_exists:
        return jsonify({"error": f"User with email {email} already exists"}), 409

    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    new_user = User(email=email, password=hashed_password, role=role)
    db.session.add(new_user)
    db.session.commit()

    access_token = create_access_token(identity={"email": email, "role": role})
    return jsonify({"access_token": access_token}), 200

@app.route("/login", methods=["POST"])
def login_user():
    email = request.json["email"]
    password = request.json["password"]

    user = User.query.filter_by(email=email, role='user').first()

    if user is None:
        return jsonify({"error": "User not found"}), 401
    if not bcrypt.check_password_hash(user.password, password):
        return jsonify({"error": "Password is incorrect"}), 401
    
    access_token = create_access_token(identity={"email": email, "role": user.role})
    return jsonify({"access_token": access_token}), 200

@app.route("/logout", methods=["POST"])
@jwt_required()
def logout_user():
    return jsonify({"message": "Logged out successfully"}), 200

@app.route("/admin/signup", methods=["POST"])
def register_admin():
    email = request.json["email"]
    password = request.json["password"]

    if password != ADMIN_SIGNUP_PASSWORD:
        return jsonify({"error": "Invalid password for admin signup"}), 401

    admin_exists = User.query.filter_by(email=email, role='admin').first() is not None

    if admin_exists:
        return jsonify({"error": f"Admin with email {email} already exists"}), 409

    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    new_admin = User(email=email, password=hashed_password, role='admin')
    db.session.add(new_admin)
    db.session.commit()

    access_token = create_access_token(identity={"email": email, "role": 'admin'})
    return jsonify({"access_token": access_token}), 200

@app.route("/admin/login", methods=["POST"])
def login_admin():
    email = request.json["email"]
    password = request.json["password"]

    admin = User.query.filter_by(email=email, role='admin').first()

    if admin is None:
        return jsonify({"error": "Admin not found"}), 401
    if not bcrypt.check_password_hash(admin.password, password):
        return jsonify({"error": "Password is incorrect"}), 401
    
    access_token = create_access_token(identity={"email": email, "role": 'admin'})
    return jsonify({"access_token": access_token}), 200

@app.route("/admin/logout", methods=["POST"])
@jwt_required()
def logout_admin():
    return jsonify({"message": "Admin logged out successfully"}), 200

if __name__ == '__main__':
    app.run(port=5555, debug=True)

