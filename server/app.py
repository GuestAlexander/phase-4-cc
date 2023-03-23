#!/usr/bin/env python3

from flask import Flask, make_response, jsonify, request
from flask_migrate import Migrate
from flask_restful import Api, Resource

from models import db, Restaurant, RestaurantPizza, Pizza

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

api = Api(app)

@app.route('/restaurants/<int:id>', methods=['GET'])
def get_restaurant(id):
    restaurant = Restaurant.query.get(id)
    
    if not restaurant:
        return make_response(jsonify({'error': 'Restaurant not found'}), 404)

    return make_response(jsonify(restaurant.to_dict()), 200)

@app.route('/restaurants/<int:id>', methods=['DELETE'])
def delete_restaurant(id):
    restaurant = Restaurant.query.get(id)

    if not restaurant:
        return make_response(jsonify({'error': 'Restaurant not found'}), 404)

    # Delete all associated RestaurantPizza objects first

    # Delete the Restaurant object itself
    db.session.delete(restaurant)
    db.session.commit()

    return make_response('', 204)


@app.route('/restaurants', methods = ['GET'])
def restaurants():
    restaurants = Restaurant.query.all()
    restaurants_dict = [restaurant.to_dict() for restaurant in restaurants]

    response = make_response(
        jsonify(restaurants_dict),
        200
    )

    return response

@app.route('/restaurant_pizzas', methods=['POST'])
def create_restaurant_pizza():
    data = request.get_json()

    if 'restaurant_id' not in data or 'pizza_id' not in data:
        return make_response(jsonify({"errors": ["validation errors"]}), 400)
    
    if 'price' not in data:
        return make_response(jsonify({"errors": ["validation errors"]}), 400)
    
    if 'price' in data and (data['price'] < 1 or data['price'] > 30):
        return make_response(jsonify({"errors": ["validation errors"]}), 400)
    

    restaurant = Restaurant.query.get(data['restaurant_id'])
    pizza = Pizza.query.get(data['pizza_id'])

    if not restaurant or not pizza:
        return make_response(jsonify({'error': 'Restaurant or Pizza not found'}), 404)

    new_restaurant_pizza = RestaurantPizza(restaurant_id=restaurant.id, pizza_id=pizza.id, price=data.get('price'))
    db.session.add(new_restaurant_pizza)
    db.session.commit()

    return make_response(jsonify({'message': 'RestaurantPizza created successfully'}), 201)


if __name__ == '__main__':
    app.run(port=5555, debug=True)

