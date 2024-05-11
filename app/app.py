




from flask import Flask, request
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from config import ApplicationConfig
from flask_cors import CORS
from models import User, db
from flask_restful import Resource, Api
from werkzeug.security import generate_password_hash

app = Flask(__name__)
CORS(app, supports_credentials=True)
bcrypt = Bcrypt(app)
app.config.from_object(ApplicationConfig)
app.config['JWT_SECRET_KEY'] = 'ce2f33f294'
jwt = JWTManager(app)
db.init_app(app)
api = Api(app)

ADMIN_EMAIL = "admin@example.com"
ADMIN_PASSWORD = "1234"

class SignUp(Resource):
    def post(self):
        email = request.json["email"]
        password = request.json["password"]

        user_exists = User.query.filter_by(email=email).first() is not None
        if user_exists:
            return {"error": f"User with email {email} already exists"}, 409

        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        new_user = User(email=email, password=hashed_password, role="user")
        db.session.add(new_user)
        db.session.commit()

        access_token = create_access_token(identity={"email": email, "role": "user"})
        return {"access_token": access_token, "role": "user"}, 200
api.add_resource(SignUp, '/signup')
    
    
class Login(Resource):
    def post(self):
        email = request.json["email"]
        password = request.json["password"]

        if email == ADMIN_EMAIL and password == ADMIN_PASSWORD:
            access_token = create_access_token(identity={"email": email, "role": "admin"})
            return {"access_token": access_token, "role": "admin"}, 200

        user = User.query.filter_by(email=email).first()

        if user is None or not bcrypt.check_password_hash(user.password, password):
            return {"error": "Invalid credentials"}, 401

        access_token = create_access_token(identity={"email": email, "role": "user"})
        return {"access_token": access_token, "role": "user"}, 200
api.add_resource(Login, '/login')

class TokenRefresh(Resource):
    @jwt_required(refresh=True)
    def post(self):
        try:
            current_user = get_jwt_identity()
            access_token = create_access_token(identity=current_user)
            return {'access_token': access_token}, 200
        except Exception as e:
            return jsonify(error=str(e)), 500



api.add_resource(TokenRefresh, '/refresh-token')

if __name__ == '__main__':
    app.run(port=5555, debug=True)

