#!/usr/bin/env python3

from flask import Flask, make_response, jsonify, request
from flask_migrate import Migrate

from models import db, Restaurant, Pizzas, Restaurant_Pizza

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def home():
    return 'Welcome to pizza Restaurant'


@app.route('/restaurants')
def restaurants():

    restaurants = []
    
    for restaurant in Restaurant.query.all():
        response_body = {
            "id" : restaurant.id,
            "name": restaurant.name,
            "address": restaurant.address
        }

        restaurants.append(response_body)
    
    response = make_response(
        jsonify(restaurants),
        200
    )

    return response


@app.route('/restaurants/<int:id>', methods = ['GET', 'DELETE'])
def restaurants_id(id):
    restaurant = Restaurant.query.filter_by(id=id).first()

    if request.method == 'GET':
        

        if restaurant == None:
            response = make_response(
                jsonify({
                    "error": "Restaurant not found"
                    }),
                404
            )
            return response
        else:


            response_body = {
                "id" : restaurant.id,
                "name" :restaurant.name,
                "address": restaurant.address,
            }

            response = make_response(
                jsonify(response_body),
                200
            )

            return response
    
    elif request.method == 'DELETE':
        db.session.delete(restaurant)
        db.session.commit()

        response_body = {
            "message" : "Restaurant deleted !!"
        }

        response = make_response(
            jsonify(response_body),
            202
        )

        return response
    
@app.route('/pizzas')
def get_pizzas():

    pizza = []

    for piz in Pizzas.query.all():

        response_body = {
            "id": piz.id,
            "name" : piz.name,
            "ingredients" : piz.ingredients
        }

        pizza.append(response_body)

        response = make_response(
            jsonify(pizza),
            200
        )

    return response


@app.route('/restaurant_pizzas', methods = ['GET', 'POST'])
def restaurant_pizzas():

    if request.method == 'GET':

        rest_piz = []

        for piz in Restaurant_Pizza.query.all():

            response_body = {
                "id" : piz.id,
                "pizza_id": piz.pizza_id,
                "restaurant_id": piz.restaurant_id,
                "price": piz.price
            }

            rest_piz.append(response_body)


            response = make_response(
                jsonify(rest_piz),
                200
            )

        return response
    
    elif request.method == 'POST':

        new_restpizza = Restaurant_Pizza(
            pizza_id = request.form.get("pizza_id"),
            restaurant_id = request.form.get("restaurant_id"),
            price = request.form.get("price")
        )
        db.session.add(new_restpizza)
        db.session.commit()

        rest_dict = new_restpizza.to_dict()

        response = make_response(
            jsonify(rest_dict),
            201
        )

        return response
    
if __name__ == '__main__':
    app.run(port=5555)
