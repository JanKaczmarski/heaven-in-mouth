from flask import session
from flask_restful import Resource, reqparse, abort
from werkzeug.security import check_password_hash
from models import Users


# Parsers that check if the request has the required fields
user_parser = reqparse.RequestParser()
user_parser.add_argument('email', type=str, required=True, help="Email cannot be blank!")
user_parser.add_argument('password', type=str, required=True, help="Password cannot be blank!")


class LoginResource(Resource):
    # Check if a user is logged in
    def get(self):
        user_id = session.get('user_id')
        if user_id:
            return {'message': 'User is logged in', 'user_id': user_id}, 200
        else:
            return {'message': 'User is not logged in'}, 401

    # Login a user
    def post(self):
        user_id = session.get('user_id')
        if user_id:
            abort(400, message='User is already logged in')

        args = user_parser.parse_args()
        user = Users.query.filter_by(email=args['email']).first()

        if not user:
            abort(404, message='User not found')

        if not check_password_hash(user.password, args['password']):
            abort(401, message='Incorrect password')

        session['user_id'] = user.user_id
        session['csrf_token'] = 'some_csrf_token'  # Generate CSRF token as needed
        session['admin'] = user.admin
        session['email'] = user.email

        return {'message': 'Logged in successfully'}, 200
