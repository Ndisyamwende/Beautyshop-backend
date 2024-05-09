from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///orders.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_name = db.Column(db.String(100), nullable=False)
    customer_email = db.Column(db.String(100), nullable=False)
    order_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    total_cost = db.Column(db.Float, nullable=False, default=0)
    products = db.relationship('OrderProduct', backref='order', lazy=True)

class OrderProduct(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    product = db.relationship('Product', backref=db.backref('order_products', lazy=True))

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)

@app.route('/checkout', methods=['POST'])
def checkout():
    data = request.get_json()
    customer_name = data.get('customer_name')
    customer_email = data.get('customer_email')
    products = data.get('products')

    if not customer_name or not customer_email:
        return jsonify({'error': 'Customer information is required'}), 400

    if not products:
        return jsonify({'error': 'No products in cart'}), 400

    order = Order(customer_name=customer_name, customer_email=customer_email)
    db.session.add(order)
    db.session.commit()

    total_cost = 0

    for product in products:
        product_id = product.get('id')
        quantity = product.get('quantity')

        if not product_id or not quantity:
            return jsonify({'error': 'Product information is required'}), 400

        product_obj = Product.query.get(product_id)
        if not product_obj:
            return jsonify({'error': 'Product not found'}), 404

        order_product = OrderProduct(order_id=order.id, product_id=product_id, quantity=quantity)
        db.session.add(order_product)
        total_cost += product_obj.price * quantity
        order.total_cost = total_cost
        db.session.commit()

        return jsonify({'message': 'Order created successfully'}), 201

if __name__ == "__main__":
    app.run(debug=True)

   
