from flask import request
from flask_restx import Resource, fields
from flask_jwt_extended import jwt_required
from datetime import datetime
from app import db
from app.models import Workspace, Booking
from app.api import api
from app.api.bookings import booking_model

ns = api.namespace('workspaces', description='Workspace operations')

# API модели
workspace_model = api.model('Workspace', {
    'id': fields.Integer(readonly=True, description='Workspace identifier'),
    'name': fields.String(required=True, description='Workspace name'),
    'description': fields.String(description='Workspace description'),
    'capacity': fields.Integer(required=True, description='Number of people'),
    'price_per_hour': fields.Float(required=True, description='Price per hour'),
    'is_available': fields.Boolean(description='Availability status'),
    'created_at': fields.DateTime(readonly=True, description='Creation timestamp')
})

workspace_create_model = api.model('WorkspaceCreate', {
    'name': fields.String(required=True, description='Workspace name'),
    'description': fields.String(description='Workspace description'),
    'capacity': fields.Integer(required=True, description='Number of people'),
    'price_per_hour': fields.Float(required=True, description='Price per hour'),
    'is_available': fields.Boolean(description='Availability status')
})

workspace_update_model = api.model('WorkspaceUpdate', {
    'name': fields.String(description='Workspace name'),
    'description': fields.String(description='Workspace description'),
    'capacity': fields.Integer(description='Number of people'),
    'price_per_hour': fields.Float(description='Price per hour'),
    'is_available': fields.Boolean(description='Availability status')
})

@ns.route('/')
class WorkspaceList(Resource):
    @ns.doc('list_workspaces',
        description='Get all workspaces'
    )
    @ns.marshal_list_with(workspace_model)
    def get(self):
        """List all workspaces"""
        return Workspace.query.all()

    @ns.doc('create_workspace',
        description='Create a new workspace',
        security='Bearer'
    )
    @ns.expect(workspace_create_model)
    @ns.marshal_with(workspace_model, code=201)
    @ns.response(400, 'Invalid input')
    @jwt_required()
    def post(self):
        """Create a new workspace"""
        data = request.get_json()
        workspace = Workspace(
            name=data['name'],
            description=data.get('description'),
            capacity=data['capacity'],
            price_per_hour=data['price_per_hour'],
            is_available=data.get('is_available', True)
        )
        db.session.add(workspace)
        db.session.commit()
        return workspace, 201

@ns.route('/<int:id>')
@ns.param('id', 'The workspace identifier')
class WorkspaceResource(Resource):
    @ns.doc('get_workspace',
        description='Get a workspace by ID'
    )
    @ns.marshal_with(workspace_model)
    @ns.response(404, 'Workspace not found')
    def get(self, id):
        """Get a workspace by ID"""
        return Workspace.query.get_or_404(id)

    @ns.doc('update_workspace',
        description='Update a workspace',
        security='Bearer'
    )
    @ns.expect(workspace_update_model)
    @ns.marshal_with(workspace_model)
    @ns.response(404, 'Workspace not found')
    @jwt_required()
    def put(self, id):
        """Update a workspace"""
        workspace = Workspace.query.get_or_404(id)
        data = request.get_json()
        
        if 'name' in data:
            workspace.name = data['name']
        if 'description' in data:
            workspace.description = data['description']
        if 'capacity' in data:
            workspace.capacity = data['capacity']
        if 'price_per_hour' in data:
            workspace.price_per_hour = data['price_per_hour']
        if 'is_available' in data:
            workspace.is_available = data['is_available']
        
        db.session.commit()
        return workspace

    @ns.doc('delete_workspace',
        description='Delete a workspace',
        security='Bearer'
    )
    @ns.response(204, 'Workspace deleted')
    @ns.response(404, 'Workspace not found')
    @jwt_required()
    def delete(self, id):
        """Delete a workspace"""
        workspace = Workspace.query.get_or_404(id)
        db.session.delete(workspace)
        db.session.commit()
        return '', 204

@ns.route('/<int:id>/bookings')
@ns.param('id', 'The workspace identifier')
class WorkspaceBookings(Resource):
    @ns.doc('get_workspace_bookings',
        description='Get all bookings for a specific workspace',
        security='Bearer'
    )
    @ns.marshal_list_with(booking_model)
    @ns.response(404, 'Workspace not found')
    @jwt_required()
    def get(self, id):
        """Get all bookings for a specific workspace"""
        workspace = Workspace.query.get_or_404(id)
        bookings = Booking.query.filter_by(workspace_id=workspace.id).filter(Booking.status != 'cancelled').filter(Booking.end_time > datetime.utcnow()).all()
        return bookings 