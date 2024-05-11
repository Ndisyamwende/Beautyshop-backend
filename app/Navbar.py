from flask import Flask, jsonify
from flask_restful import Api, Resource

app = Flask(__name__)
api = Api(app)

class Navbar(Resource):
    def get(self):
        navbar_items = [
            {'id': 1, 'label': 'Home', 'url': '/home'},
            {'id': 2, 'label': 'Services', 'url': '/services'},
            {'id': 3, 'label': 'Products', 'url': '/products'},
            {'id': 4, 'label': 'About', 'url': '/about'},
            {'id': 5, 'label': 'Contact', 'url': '/contact'}
        ]
        return jsonify({'navbar_items': navbar_items})

api.add_resource(Navbar, '/navbar')

if __name__ == '__main__':
    app.run(debug=True)