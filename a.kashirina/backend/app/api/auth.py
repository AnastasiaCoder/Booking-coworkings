from flask import request
from flask_restx import Resource, fields
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from app.models import User
from app.api import api
from app import db

ns = api.namespace('auth', description='Authentication operations')

auth_model = api.model('Auth', {
    'email': fields.String(required=True, description='User email'),
    'password': fields.String(required=True, description='User password')
})

profile_model = api.model('Profile', {
    'first_name': fields.String(description='User first name'),
    'last_name': fields.String(description='User last name')
})

password_model = api.model('Password', {
    'current_password': fields.String(required=True, description='Current password'),
    'new_password': fields.String(required=True, description='New password')
})

@ns.route('/login')
class Login(Resource):
    @ns.doc('login')
    @ns.expect(auth_model)
    def post(self):
        """Login user and return JWT token"""
        try:
            data = request.get_json()
            if not data:
                return {'message': 'No input data provided'}, 400

            if not data.get('email') or not data.get('password'):
                return {'message': 'Email and password are required'}, 400

            user = User.query.filter_by(email=data['email']).first()
            
            if user and user.check_password(data['password']):
                access_token = create_access_token(identity=user.id)
                return {'access_token': access_token}, 200
            
            return {'message': 'Invalid email or password'}, 401
        except Exception as e:
            return {'message': str(e)}, 500

@ns.route('/register')
class Register(Resource):
    @ns.doc('register')
    @ns.expect(auth_model)
    def post(self):
        """Register a new user"""
        try:
            data = request.get_json()
            if not data:
                return {'message': 'No input data provided'}, 400

            if not data.get('email') or not data.get('password'):
                return {'message': 'Email and password are required'}, 400
            
            if User.query.filter_by(email=data['email']).first():
                return {'message': f"User with email {data['email']} already exists"}, 400
            
            user = User(email=data['email'])
            user.set_password(data['password'])
            
            db.session.add(user)
            db.session.commit()
            
            access_token = create_access_token(identity=user.id)
            return {'access_token': access_token}, 201
        except Exception as e:
            db.session.rollback()
            return {'message': str(e)}, 500

@ns.route('/me')
class UserProfile(Resource):
    @ns.doc('get_profile')
    @jwt_required()
    def get(self):
        """Get current user profile"""
        try:
            current_user_id = get_jwt_identity()
            user = User.query.get_or_404(current_user_id)
            return user.to_dict()
        except Exception as e:
            return {'message': str(e)}, 500

    @ns.doc('update_profile')
    @ns.expect(profile_model)
    @jwt_required()
    def put(self):
        """Update user profile"""
        try:
            current_user_id = get_jwt_identity()
            user = User.query.get_or_404(current_user_id)
            
            data = request.get_json()
            if not data:
                return {'message': 'No input data provided'}, 400

            if 'first_name' in data:
                user.first_name = data['first_name']
            if 'last_name' in data:
                user.last_name = data['last_name']

            db.session.commit()
            return user.to_dict()
        except Exception as e:
            db.session.rollback()
            return {'message': str(e)}, 500

@ns.route('/me/password')
class UserPassword(Resource):
    @ns.doc('change_password')
    @ns.expect(password_model)
    @jwt_required()
    def put(self):
        """Change user password"""
        try:
            current_user_id = get_jwt_identity()
            user = User.query.get_or_404(current_user_id)
            
            data = request.get_json()
            if not data:
                return {'message': 'No input data provided'}, 400

            if not data.get('current_password') or not data.get('new_password'):
                return {'message': 'Current password and new password are required'}, 400

            if not user.check_password(data['current_password']):
                return {'message': 'Current password is incorrect'}, 401

            user.set_password(data['new_password'])
            db.session.commit()
            
            return {'message': 'Password updated successfully'}, 200
        except Exception as e:
            db.session.rollback()
            return {'message': str(e)}, 500 