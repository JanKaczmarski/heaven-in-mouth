from flask import jsonify
from flask_restful import Resource, reqparse, abort
from werkzeug.security import generate_password_hash
from models import db, Users


# Parsers that check if the request has the required fields
user_parser = reqparse.RequestParser()
user_parser.add_argument('name', type=str, required=True, help="Name cannot be blank!")
user_parser.add_argument('email', type=str, required=True, help="Email cannot be blank!")
user_parser.add_argument('phone', type=str, required=True, help="Phone cannot be blank!")
user_parser.add_argument('password', type=str, required=True, help="Password cannot be blank!")


class UserResource(Resource):
    # Get all users or a specific user
    def get(self, user_id=None):
        if user_id:
            user = db.session.get(Users, user_id)
            if not user:
                abort(404, message='User not found')

            return jsonify(user.to_json())
        else:
            users = Users.query.all()
            return jsonify([user.to_json() for user in users])

    # Create a new user
    def post(self):
        args = user_parser.parse_args()
        new_user = Users(
            name=args['name'],
            email=args['email'],
            phone=args['phone'],
            password=generate_password_hash(args['password'])
        )
        db.session.add(new_user)
        db.session.commit()
        return {'message': 'User created'}, 201

    # Update a user
    def put(self, user_id):
        user = db.session.get(Users, user_id)
        if not user:
            abort(404, message='User not found')

        args = user_parser.parse_args()
        user.name = args['name']
        user.email = args['email']
        user.phone = args['phone']
        user.password = generate_password_hash(args['password'])
        db.session.commit()
        return {'message': 'User updated'}

    # Delete a user
    def delete(self, user_id):
        user = db.session.get(Users, user_id)
        if not user:
            abort(404, message='User not found')

        db.session.delete(user)
        db.session.commit()
        return {'message': 'User deleted'}