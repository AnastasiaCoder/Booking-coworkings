from flask import request
from flask_restx import Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models import User
from app.api import api

ns = api.namespace('users', description='User operations')

user_model = api.model('User', {
    'id': fields.Integer(readonly=True),
    'email': fields.String(required=True, description='User email'),
    'first_name': fields.String(description='First name'),
    'last_name': fields.String(description='Last name'),
    'phone': fields.String(description='Phone number'),
    'company': fields.String(description='Company name')
})

@ns.route('/')
class UserList(Resource):
    @ns.doc('list_users')
    @ns.marshal_list_with(user_model)
    @jwt_required()
    def get(self):
        """List all users"""
        return User.query.all()

    @ns.doc('create_user')
    @ns.expect(user_model)
    @ns.marshal_with(user_model, code=201)
    def post(self):
        """Create a new user"""
        data = request.get_json()
        if User.query.filter_by(email=data['email']).first():
            api.abort(400, f"User with email {data['email']} already exists")
        
        user = User(
            email=data['email'],
            first_name=data.get('first_name'),
            last_name=data.get('last_name'),
            phone=data.get('phone'),
            company=data.get('company')
        )
        user.set_password(data['password'])
        
        db.session.add(user)
        db.session.commit()
        return user, 201

@ns.route('/<int:id>')
@ns.param('id', 'The user identifier')
class UserResource(Resource):
    @ns.doc('get_user')
    @ns.marshal_with(user_model)
    @jwt_required()
    def get(self, id):
        """Get a user by ID"""
        return User.query.get_or_404(id)

    @ns.doc('update_user')
    @ns.expect(user_model)
    @ns.marshal_with(user_model)
    @jwt_required()
    def put(self, id):
        """Update a user"""
        user = User.query.get_or_404(id)
        data = request.get_json()
        
        if 'email' in data:
            user.email = data['email']
        if 'first_name' in data:
            user.first_name = data['first_name']
        if 'last_name' in data:
            user.last_name = data['last_name']
        if 'phone' in data:
            user.phone = data['phone']
        if 'company' in data:
            user.company = data['company']
        if 'password' in data:
            user.set_password(data['password'])
        
        db.session.commit()
        return user

    @ns.doc('delete_user')
    @ns.response(204, 'User deleted')
    @jwt_required()
    def delete(self, id):
        """Delete a user"""
        user = User.query.get_or_404(id)
        db.session.delete(user)
        db.session.commit()
        return '', 204

@ns.route('/me')
class UserMe(Resource):
    @ns.doc('get_current_user')
    @jwt_required()
    def get(self):
        """Get current user profile"""
        current_user_id = get_jwt_identity()
        user = User.query.get_or_404(current_user_id)
        return user.to_dict()

    @ns.doc('update_current_user')
    @ns.expect(user_model)
    @jwt_required()
    def put(self):
        """Update current user profile"""
        current_user_id = get_jwt_identity()
        user = User.query.get_or_404(current_user_id)
        data = request.get_json()
        if 'first_name' in data:
            user.first_name = data['first_name']
        if 'last_name' in data:
            user.last_name = data['last_name']
        if 'phone' in data:
            user.phone = data['phone']
        if 'company' in data:
            user.company = data['company']
        db.session.commit()
        return user.to_dict()

@ns.route('/me/password')
class UserMePassword(Resource):
    @ns.doc('change_current_user_password')
    @jwt_required()
    def put(self):
        """Change current user password"""
        current_user_id = get_jwt_identity()
        user = User.query.get_or_404(current_user_id)
        data = request.get_json()
        if not data.get('current_password') or not data.get('new_password'):
            return {'message': 'Current password and new password are required'}, 400
        if not user.check_password(data['current_password']):
            return {'message': 'Current password is incorrect'}, 401
        user.set_password(data['new_password'])
        db.session.commit()
        return {'message': 'Password updated successfully'}, 200 