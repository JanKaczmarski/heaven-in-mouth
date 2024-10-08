from flask_restful import Resource, reqparse, abort
from models import db, Restaurants
from helpers import geocode_address

# Parsers that check if the request has the required fields
restaurant_parser = reqparse.RequestParser()
restaurant_parser.add_argument('name', type=str, required=True, help="Name cannot be blank!")
restaurant_parser.add_argument('address', type=str, required=True, help="Address cannot be blank!")
restaurant_parser.add_argument('phone', type=str, required=True, help="Phone cannot be blank!")


class RestaurantResource(Resource):
    # Get all restaurants or a specific restaurant
    def get(self, restaurant_id=None):
        if restaurant_id:
            restaurant = db.session.get(Restaurants, restaurant_id)
            if not restaurant:
                abort(404, message='Restaurant not found')
            return restaurant.to_json(True), 200
        else:
            restaurants = Restaurants.query.all()
            return [restaurant.to_json() for restaurant in restaurants], 200

    # Create a new restaurant
    def post(self):
        args = restaurant_parser.parse_args()
        address = args['address']
        try:
            geo_data = geocode_address(address)
        except Exception as e:
            abort(400, message=str(e))

        new_restaurant = Restaurants(
            name=args['name'],
            address=address,
            phone=args['phone'],
            longitude=geo_data['longitude'],
            latitude=geo_data['latitude']
        )
        db.session.add(new_restaurant)
        db.session.commit()
        return {'message': 'Restaurant created'}, 201

    # Update a restaurant
    def put(self, restaurant_id):
        restaurant = db.session.get(Restaurants, restaurant_id)
        if not restaurant:
            abort(404, message='Restaurant not found')

        args = restaurant_parser.parse_args()
        restaurant.name = args['name']
        restaurant.phone = args['phone']
        restaurant.address = args['address']

        # Update the geocoding data
        try:
            geo_data = geocode_address(args['address'])
            restaurant.longitude = geo_data['longitude']
            restaurant.latitude = geo_data['latitude']
        except Exception as e:
            abort(400, message=str(e))

        db.session.commit()
        return {'message': 'Restaurant updated'}, 200

    # Delete a restaurant
    def delete(self, restaurant_id):
        restaurant = db.session.get(Restaurants, restaurant_id)
        if not restaurant:
            abort(404, message='Restaurant not found')

        db.session.delete(restaurant)
        db.session.commit()
        return {'message': 'Restaurant deleted'}, 200
