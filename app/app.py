
from flask import Flask, request, jsonify, make_response
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
#from config import ApplicationConfig
from flask_cors import CORS
from models import User, OrderProduct, OrderProduct, db, Product, ProductAnalytics
from flask_restful import Resource, Api
from werkzeug.security import generate_password_hash
from dotenv import load_dotenv

import os

load_dotenv()

app = Flask(__name__)
migrate = Migrate(app, db)
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
    


class TokenRefresh(Resource):
    @jwt_required(refresh=True)
    def post(self):
        try:
            current_user = get_jwt_identity()
            access_token = create_access_token(identity=current_user)
            return {'access_token': access_token}, 200
        except Exception as e:
            return jsonify(error=str(e)), 500
        


class OrderProductsResource(Resource):
    def get(self):
        order_products = []
        for product in OrderProduct.query.all():
            product_dict = {
                "id": product.id,
                "product_name": product.product_name,
                "price": product.price,
                "quantity": product.quantity,
            }
            order_products.append(product_dict)
        return jsonify(order_products)

def post(self):
        data = request.json
        product_name = data.get('product_name')
        price = data.get('price')
        quantity = data.get('quantity')

        if not product_name or not price or not quantity:
            return jsonify({'error': 'Missing data!'}), 400

        new_product = OrderProduct(product_name=product_name, price=price, quantity=quantity)
        db.session.add(new_product)
        db.session.commit()

        return jsonify({'message': 'Product added to order successfully!'}), 201

class OrderProductResource(Resource):
    def delete(self, product_id):
        product = OrderProduct.query.get(product_id)
        if product:
            db.session.delete(product)
            db.session.commit()
            return jsonify({'message': 'Product deleted from order successfully!'})
        else:
            return jsonify({'error': 'Product not found!'}), 404

    def put(self, product_id):
        product = OrderProduct.query.get(product_id)
        if not product:
            return jsonify({'error': 'Product not found!'}), 404

        data = request.json
        product_name = data.get('product_name')
        price = data.get('price')
        quantity = data.get('quantity')

        if product_name:
            product.product_name = product_name
        if price:
            product.price = price
        if quantity:
            product.quantity = quantity

        db.session.commit()
        return jsonify({'message': 'Product updated successfully!'})

api.add_resource(SignUp, '/signup')
api.add_resource(Login, '/login')
api.add_resource(TokenRefresh, '/refresh-token')
api.add_resource(OrderProductsResource, '/order-products', '/order-products/<int:product_id>')
api.add_resource(OrderProductResource, '/order-products')

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)