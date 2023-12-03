from models import Restaurant, Restaurant_Pizza, Pizzas, db
from faker import Faker
import random
from app import app


fake = Faker()


with app.app_context():
    Restaurant.query.delete()
    Restaurant_Pizza.query.delete()
    Pizzas.query.delete()
    db.session.commit()

    restaurants = []

    for item in range(10):
        restaurant = Restaurant(
            name = f'The {fake.name()}',
            address = fake.address()
        )

        restaurants.append(restaurant)

        db.session.add(restaurant)
        db.session.commit()

    
    pizzas =[]

    for item in range(10):
        pizz = Pizzas(

            name = f'{fake.name()}',
            ingredients = fake.sentence(),
        )

        pizzas.append(pizz)

        db.session.add(pizz)
        db.session.commit()

    rest_pizza = []

    for item in range(10):
        rest = Restaurant_Pizza(
            restaurant_id = random.randint(1,10),
            pizza_id = random.randint(1,10),
            price = random.randint(1,30)
        )

        rest_pizza.append(rest)

        db.session.add(rest)
        db.session.commit()