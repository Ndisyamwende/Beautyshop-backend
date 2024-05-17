from flask import Flask, request, jsonify
from flask import Flask, request, jsonify, make_response
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
#from config import ApplicationConfig
from flask_cors import CORS
from .models import User, Product, OrderItem,  db, Order, Category, Payment,  Contact
from flask_restful import Resource, Api
from werkzeug.security import generate_password_hash
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
app.config['JWT_SECRET_KEY'] = 'ce2f33f294'
jwt = JWTManager(app)
db.init_app(app)
api = Api(app)

ADMIN_EMAIL = "admin@example.com"
ADMIN_PASSWORD = "admin"
class SignUp(Resource):
    def post(self):
        username = request.json.get("username")
        email = request.json.get("email")
        password = request.json.get("password")

        if not username or not email or not password:
            return {"error": "Username, email, and password are required"}, 400

        user_exists = User.query.filter_by(email=email).first() is not None
        if user_exists:
            return {"error": f"User with email {email} already exists"}, 409

        if email == ADMIN_EMAIL and password == ADMIN_PASSWORD:
            role = "admin"
        else:
            role = "user"

        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        new_user = User(email=email, password=hashed_password, role=role, username=username)
        db.session.add(new_user)
        db.session.commit()

        access_token = create_access_token(identity={"id": new_user.id, "email": email, "role": role})
        return {"access_token": access_token, "role": role}, 200
api.add_resource(SignUp, '/signup')
    
class Login(Resource):
    def post(self):
        email = request.json.get("email")
        password = request.json.get("password")

        if not email or not password:
            return {"error": "Email and password are required"}, 400

        if email == ADMIN_EMAIL:
            if password == ADMIN_PASSWORD:
                access_token = create_access_token(identity={"email": email, "role": "admin", "id": "admin"})
                return {"access_token": access_token, "role": "admin"}, 200
            else:
                return {"error": "Incorrect password"}, 401

        user = User.query.filter_by(email=email).first()

        if user is None:
            return {"error": "Email not found"}, 404

        if not bcrypt.check_password_hash(user.password, password):
            return {"error": "Incorrect password"}, 401

        access_token = create_access_token(identity={"id": user.id, "email": email, "role": user.role})
        return {"access_token": access_token, "role": user.role}, 200


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
        
api.add_resource(TokenRefresh, '/tokenrefresh')
        

#User routes
#the get is for admins only to view their user data base
class UserResource(Resource):
    # does not work but smae code works in another port
    @jwt_required()
    def get(self):
       claims = get_jwt_identity()
       user_id = claims['id']
       user_role = claims['role']

       if user_role != 'admin':
            return {"error": "Unauthorized"}, 403
       
       users = [user.to_dict() for user in User.query.all()]
       return make_response(users, 200)
    
    #works
    @jwt_required()
    def post(self):
        claims = get_jwt_identity()
        if claims['role'] != 'admin':
            return {"error": "Only admins can create add new employees"}, 403
        
        data = request.get_json()
        if not data:
            return {"error": "Missing data in request"}, 400
        
        hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
        user = User(
            username=data['username'], 
            email=data['email'],
            role=data['role'],
            password=hashed_password,
            department=data['department'],
            )
        
        db.session.add(user)
        db.session.commit()
        return make_response(user.to_dict(), 201)
api.add_resource(UserResource, '/user')

 #the patch for the user to edit their profile  and get to view their profile  
#the get works
class UserById(Resource):
    @jwt_required()
    def get(self, id):
        user = User.query.filter_by(id=id).first()
        if user is None:
            return {"error": "User not found"}, 404
        response_dict = user.to_dict()
        return make_response(response_dict, 200)
    
    #works
    @jwt_required()
    def patch(self, id):
        claims = get_jwt_identity()
        user = User.query.filter_by(id=id).first()
        if user is None:
            return {"error": "User not found"}, 404

        data = request.get_json()
        if claims['role'] == 'admin':
            if all(key in data for key in ['username', 'email', 'password', 'department', 'role']):
                try:   
                    user.username = data['username']
                    user.email = data['email']
                    user.department = data['department']
                    user.role = data['role']
                    user.password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
                    db.session.commit()
                    return make_response(user.to_dict(), 200)
                
                except AssertionError:
                    return {"errors": ["validation errors"]}, 400
            else:
                return {"errors": ["validation errors"]}, 400
        elif claims['role'] == 'user' and any(key in data for key in ['password', 'username', 'email']):
            try:
                if 'password' in data:
                    user.password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
                if 'username' in data:
                    user.name = data['username']
                if 'email' in data:
                    user.email = data['email']
                db.session.commit()
                return make_response(user.to_dict(), 200)
            except AssertionError:
                return {"errors": ["validation errors"]}, 400
        else:
            return {"error": "Unauthorized"}, 403

api.add_resource(UserById, '/users/<int:id>')

class OrderResource(Resource):
    #works
    @jwt_required()
    def get(self):
       claims = get_jwt_identity()
       user_id = claims['id']
       user_role = claims['role']

       if user_role != 'admin':
            return {"error": "Unauthorized"}, 403
       
       order = [Order.to_dict() for user in Order.query.all()]
       return make_response(order, 200)
    
api.add_resource(OrderResource, '/orders')


class OrderById(Resource):
   #works
    @jwt_required()
    def get(self, id):
        order = Order.query.filter_by(id=id).first()
        if order is None:
            return{"error": "order not found"}, 404
        response_dict = order.to_dict()
        return make_response(response_dict, 200)
    
api.add_resource(OrderById, '/order/<int:id>')


        
class OrderItemResource(Resource):
    #works
    def get(self):
        orderitems = [orderitem.to_dict() for orderitem in OrderItem.query.all()]
        return make_response({"order_items": orderitems}, 200)


#works
    def post(self):
            data = request.get_json()
            if not data:
                return {"error": "Missing data in request"}, 400
            
            required_fields = ['order_id', 'product_id', 'quantity', 'price']
            for field in required_fields:
                if field not in data:
                    return {"error": f"Missing field: {field}"}, 400
            
            orderitem = OrderItem(
                order_id=data['order_id'],
                product_id=data['product_id'],
                quantity=data['quantity'],
                price=data['price']
            )
            
            db.session.add(orderitem)
            db.session.commit()
            
            return (orderitem.to_dict()), 201

api.add_resource(OrderItemResource, '/orderitem')

class OrderItemById(Resource):
    #works
    def delete(self, id):
        product = Product.query.get(id)
        if product is None:
            return {"error": "Product not found"}, 404
        
        # Delete the product
        db.session.delete(product)
        db.session.commit()
        
        return jsonify({'message': 'Product deleted successfully'})


api.add_resource(OrderItemById, '/orderitem/<int:id>')

class OrderItemPatch(Resource):
    def patch(self, product_id):
        # Get the order item by its ID
        order_item = OrderItem.query.get(product_id)
        if not order_item:
            return jsonify({'error': 'Order item not found!'}), 404

        # Get the value to add or subtract from the quantity
        data = request.json
        quantity_change = data.get('quantity_change')
        if not quantity_change:
            return jsonify({'error': 'Quantity change not provided!'}), 400

        # Update the quantity of the order item
        new_quantity = order_item.quantity + quantity_change
        if new_quantity < 0:
            return jsonify({'error': 'Invalid quantity!'}), 400

        order_item.quantity = new_quantity
        db.session.commit()

        return jsonify({'message': 'Quantity updated successfully', 'new_quantity': new_quantity})

# Add the route to your API
api.add_resource(OrderItemPatch, '/orderitem/<int:product_id>/patch')

#class routes
class Contact(Resource):
    #the get is for admins to view all messages
    @jwt_required
    def get(self):
       claims = get_jwt_identity()
       user_id = claims['id']
       user_role = claims['role']

       if user_role != 'admin':
            return {"error": "Unauthorized"}, 403
       
       contacts = [contacts.to_dict() for contact in Contact.query.all()]
       return make_response(contacts, 200)
    
    #for a n individual user to create a message 
    @jwt_required
    def post(self):
        claims = get_jwt_identity()
        if claims['role'] != 'user':
            return {"error": "Only user can add new messages"}, 403
        
        data = request.get_json()
        if not data:
            return {"error": "Missing data in request"}, 400
        
        
        contact = Contact(
            username=data['username'], 
            email=data['email'],
            message=data['message'],
            )
        
        db.session.add(contact)
        db.session.commit()
        return make_response(contact.to_dict(), 201)
    
api.add_resource(Contact,'/contact')

#for an indiviual to get their own messages
class ContactById(Resource):
    def get(self, id):
        contact = Contact.query.filter_by(id=id).first()
        if contact is None:
            return {"error": "User not found"}, 404
        response_dict = contact.to_dict()
        return make_response(response_dict, 200)
    
    
api.add_resource(ContactById,'/contact/<int:id>') 



class ProductResource(Resource):
    @jwt_required()
    def get(self):
        claims =get_jwt_identity()
        user_id = claims['id']
        user_role = claims['role']

        if user_role != 'admin':
            return {"error": "Unauthorized"}, 403
    
        products = [product.to_dict() for product in Product.query.all()]
        return make_response(products, 200)
    
    #works
    @jwt_required()
    def post(self):
        claims = get_jwt_identity()
        if claims['role'] != 'admin':
            return {"error": "Only admins can create new products"}, 403
        
        
        data= request.get_json()
        if not data:
            return {"error": "Missing data in request"}, 400
        
        required_fields = ['name', 'gender', 'description', 'price', 'quantity_available', 'image']
        for field in required_fields:
            if field not in data:
                return {"error": f"Missing field: {field}"}, 400
        
        product = Product(
            name=data['name'], 
            gender=data['gender'],
            description=data['description'],
            price=data['price'],
            quantity_available=data['quantity_available'],
            image=data['image']
            )
        
        db.session.add(product)
        db.session.commit()
        return make_response(product.to_dict(), 201)
    
api.add_resource(ProductResource, '/product')

#Product by name, this is for the search bar
class ProductByName(Resource):
    #works
    def get(self, name):
        product = Product.query.filter_by(name=name).first()
        if product is None:
            return{"error": "Product not found"}, 404
        response_dict = product.to_dict()
        return make_response(response_dict, 200)
    
api.add_resource(ProductByName, '/product/<string:name>')



#product by category also for the searchbar and home page
class ProductByCategory(Resource):
    #not sure its giving error product not found
    def get(self, category):
        products = Product.query.filter_by(category_name=category).all()
        if not products:
            return {"error": f"No products found for category '{category}'"}, 404

        response_dict = [product.to_dict() for product in products]
        return make_response(response_dict, 200)

api.add_resource(ProductByCategory, '/product/<string:category>')
    
    
#this routes are only for admins,the get is for users to be used for product
class ProductById(Resource):
    #works
    @jwt_required()
    def get(self, id):
        product = Product.query.filter_by(id=id).first()
        if product is None:
            return {"error": "Product not found"}, 404
        response_dict = product.to_dict()
        return make_response(response_dict, 200)
    
    #works
    @jwt_required ()
    def delete(self, id):
            product = Product.query.filter_by(id=id).first()
            if product is None:
                return{"error": "Product not found"}, 404
            
            product = Product.query.get_or_404(id)
            db.session.delete(product)
            db.session.commit()
            return jsonify({'message': 'Product delete successfully'})
    
    @jwt_required()
    #works
    def patch(self, id):
        claims = get_jwt_identity()
        product = Product.query.filter_by(id=id).first()
        if product is None:
            return {"error": "Product not found"}, 404

        data = request.get_json()
        if not data:
            return {"error": "Missing data in request"}, 400

        for field in ['name', 'gender', 'description', 'price', 'quantity_available', 'image']:
            if field in data:
                setattr(product, field, data[field])

        try:
            db.session.commit()
            return make_response(product.to_dict(), 200)
        except AssertionError:
            return {"errors": ["Validation errors"]}, 400

       
api.add_resource(ProductById, '/products/<int:id>')

# get by filter for the search bar and to be able to filter the gender  
class ProductFilter(Resource):
    #works
    def get(self, gender=None):
        if gender:
            if gender.lower() not in ['male', 'female']:
                return {"error": "Invalid gender"}, 400
            
            products = Product.query.filter_by(gender=gender.capitalize()).all()
        else:
            products = Product.query.all()

        products_list = [product.to_dict() for product in products]

        return make_response(products_list, 200)

api.add_resource(ProductFilter, '/filter', '/filter/<string:gender>')


# get all is for admins to see all the categories and to create a new category
class CategoryResource(Resource):
    #works
    def get(self):
        categories = [category.to_dict() for category in Category.query.all()]
        return make_response(categories, 200)
    
    
    #works
    @jwt_required()
    def post(self):
        claims = get_jwt_identity()
        if claims['role'] != 'admin':
            return {"error": "Only admins can create new categories"}, 403
        
        data = request.get_json()
        if not data:
            return {"error": "Missing data in request"}, 400
        
        category = Category(
            name=data['name'], 
            )
        
        db.session.add(category)
        db.session.commit()
        return make_response(category.to_dict(), 201)
       
api.add_resource(CategoryResource, '/category')

class CategoryById(Resource):
    #works
    @jwt_required()
    def delete(self, id):
        claims = get_jwt_identity()
        if claims['role'] != 'admin':
            return {"error": "Only admins can delete categories"}, 403
        
        category = Category.query.get_or_404(id)
        db.session.delete(category)
        db.session.commit()
        return jsonify({'message': 'Category deleted successfully'})

api.add_resource(CategoryById, '/category/<int:id>')

class PaymentResource(Resource):
    #works
    def post(self):
        data = request.get_json()
        if not data:
            return {"error": "Missing data in request"}, 400

        try:
            payment = Payment(
                amount=data['amount'],
                method=data['method'],
                status=data['status'],
                order_id=data['order_id']
            )

            db.session.add(payment)
            db.session.commit()
            return make_response(payment.to_dict(), 201)

        except KeyError as e:
            return {"error": f"Missing field in data: {str(e)}"}, 400
        except ValueError as e:
            return {"error": str(e)}, 400

api.add_resource(PaymentResource, '/payment')



if __name__ == '__main__':
    app.run(debug=True, port=5500)









