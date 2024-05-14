
from flask import Flask, request, jsonify

from flask import Flask, request, jsonify, make_response
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
#from config import ApplicationConfig
from flask_cors import CORS
from models import User, db, Product, OrderProduct
from flask_restful import Resource, Api
from werkzeug.security import generate_password_hash
from models import db,Contact
from dotenv import load_dotenv

import os


app = Flask(__name__)
migrate = Migrate(app, db)
CORS(app, supports_credentials=True)
bcrypt = Bcrypt(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False
load_dotenv()
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')

#app.config.from_object(ApplicationConfig)
#app.config['JWT_SECRET_KEY'] = 'ce2f33f294'
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

# class ContactResource(Resource):
#     def get(self, contact_id=None):
#         if contact_id:
#             contact = Contact.query.get(contact_id)
#             if not contact:
#                 return {'error': 'Contact not found'}, 404
#             return {
#                 'id': contact.id,
#                 'name': contact.name,
#                 'email': contact.email,
#                 'message': contact.message
#             }
#         else:
#             contacts = Contact.query.all()
#             contact_list = []
#             for contact in contacts:
#                 contact_list.append({
#                     'id': contact.id,
#                     'name': contact.name,
#                     'email': contact.email,
#                     'message': contact.message
#                 })
#             return {'contacts': contact_list}

#     def post(self):
#         data = request.json
#         new_contact = Contact(name=data['name'], email=data['email'], message=data['message'])
#         db.session.add(new_contact)
#         db.session.commit()
#         return {'message': 'Contact created successfully'}, 201

#     def put(self, contact_id):
#         contact = Contact.query.get(contact_id)
#         if not contact:
#             return {'error': 'Contact not found'}, 404
#         data = request.json
#         contact.name = data.get('name', contact.name)
#         contact.email = data.get('email', contact.email)
#         contact.message = data.get('message', contact.message)
#         db.session.commit()
#         return {'message': 'Contact updated successfully'}

#     def delete(self, contact_id):
#         contact = Contact.query.get(contact_id)
#         if not contact:
#             return {'error': 'Contact not found'}, 404
#         db.session.delete(contact)
#         db.session.commit()
#         return {'message': 'Contact deleted successfully'}

# api.add_resource(ContactResource, '/contacts', '/contacts/<int:contact_id>')




#Product Routes
#post is to create a new product and get to view all products, also only admins can use this routes
class ProductResource(Resource):
    def get(self):
        products = [product.serialize() for product in Product.query.all()]
        return make_response(products, 200)
    
    def post(self):
        pass
    
api.add_resource(ProductResource, '/product')

#Product by name, this is for the search bar
class ProductByName(Resource):
    def get(self, name):
        product = Product.query.filter_by(name=name).first()
        if product is None:
            return{"error": "Product not found"}, 404
        response_dict = product.serialize()
        return make_response(response_dict, 200)
    
api.add_resource(ProductByName, '/product/<string:name>')



#product by category also for the searchbar and home page
class ProductByCategory(Resource):
    def get(self, category):
        product = Product.query.filter_by(category_name=category).all()
        if product is None:
            return{"error": "Product not found"}, 404
        response_dict = product.serialize()
        return make_response(response_dict, 200)
    
api.add_resource(ProductByCategory, '/product/<string:category>')
    
    
#this routes are only for admins,the get is for users to be used for product
class ProductById(Resource):
    def get(self, id):
        product = Product.query.filter_by(id=id).first()
        if product is None:
            return{"error": "Product not found"}, 404
        response_dict = product.serialize()
        return make_response(response_dict, 200)
    
    def delete(self, id):
        product = Product.query.filter_by(id=id).first()
        if product is None:
            return{"error": "Product not found"}, 404
        
        product = Product.query.get_or_404(id)
        db.session.delete(product)
        db.session.commit()
        return jsonify({'message': 'Product delete successfully'})
    
    def patch(self, id):
        pass
       
api.add_resource(ProductById, '/products/<int:id>')

# get by filter for the search bar and to be able to filter the gender and price range and 
class ProductFilter(Resource):
    def get(self):
        pass

api.add_resource(ProductFilter, '/filter')





if __name__ == '__main__':
    app.run(debug=True, port=5500)