from flask import request
from flask_restx import Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime
from app import db
from app.models import Booking, Workspace
from app.api import api
from app.helpers import parse_iso_datetime

ns = api.namespace('bookings', description='Booking operations')

# API модели
booking_model = api.model('Booking', {
    'id': fields.Integer(readonly=True, description='Booking identifier'),
    'user_id': fields.Integer(required=True, description='User ID'),
    'workspace_id': fields.Integer(required=True, description='Workspace ID'),
    'workspace_name': fields.String(attribute='workspace.name', readonly=True, description='Name of the workspace'),
    'start_time': fields.DateTime(required=True, description='Start time (ISO 8601 format with UTC timezone)'),
    'end_time': fields.DateTime(required=True, description='End time (ISO 8601 format with UTC timezone)'),
    'status': fields.String(description='Booking status (pending, confirmed, cancelled)'),
    'created_at': fields.DateTime(readonly=True, description='Creation timestamp')
})

booking_create_model = api.model('BookingCreate', {
    'workspace_id': fields.Integer(required=True, description='Workspace ID'),
    'start_time': fields.DateTime(required=True, description='Start time (ISO 8601 format with UTC timezone)'),
    'end_time': fields.DateTime(required=True, description='End time (ISO 8601 format with UTC timezone)')
})

booking_update_model = api.model('BookingUpdate', {
    'start_time': fields.DateTime(description='Start time (ISO 8601 format with UTC timezone)'),
    'end_time': fields.DateTime(description='End time (ISO 8601 format with UTC timezone)'),
    'status': fields.String(description='Booking status (pending, confirmed, cancelled)')
})

@ns.route('/')
class BookingList(Resource):
    @ns.doc('list_bookings',
        description='Get all bookings for the current user',
        security='Bearer'
    )
    @ns.marshal_list_with(booking_model)
    @jwt_required()
    def get(self):
        """List all bookings for the current user"""
        current_user_id = get_jwt_identity()
        return Booking.query.filter_by(user_id=current_user_id).all()

    @ns.doc('create_booking',
        description='Create a new booking',
        security='Bearer'
    )
    @ns.expect(booking_create_model)
    @ns.marshal_with(booking_model, code=201)
    @ns.response(400, 'Invalid input or overlapping booking')
    @ns.response(404, 'Workspace not found')
    @jwt_required()
    def post(self):
        """Create a new booking"""
        data = request.get_json()
        current_user_id = get_jwt_identity()
        
        # Проверка workspace существует и свободен
        workspace = Workspace.query.get_or_404(data['workspace_id'])
        if not workspace.is_available:
            api.abort(400, "Workspace is not available")
        
        start_time = parse_iso_datetime(data['start_time'])
        end_time = parse_iso_datetime(data['end_time'])
        
        # Нет ли совпадающих bookings
        overlapping = Booking.query.filter(
            Booking.workspace_id == data['workspace_id'],
            Booking.status != 'cancelled',
            ((Booking.start_time <= start_time) & (Booking.end_time > start_time)) |
            ((Booking.start_time < end_time) & (Booking.end_time >= end_time)) |
            ((Booking.start_time >= start_time) & (Booking.end_time <= end_time))
        ).first()
        
        if overlapping:
            api.abort(400, "There is an overlapping booking for this workspace")
        
        booking = Booking(
            user_id=current_user_id,
            workspace_id=data['workspace_id'],
            start_time=start_time,
            end_time=end_time,
            status='pending'
        )
        
        db.session.add(booking)
        db.session.commit()
        return booking, 201

@ns.route('/<int:id>')
@ns.param('id', 'The booking identifier')
class BookingResource(Resource):
    @ns.doc('get_booking',
        description='Get a booking by ID',
        security='Bearer'
    )
    @ns.marshal_with(booking_model)
    @ns.response(403, 'Not authorized to access this booking')
    @ns.response(404, 'Booking not found')
    @jwt_required()
    def get(self, id):
        """Get a booking by ID"""
        current_user_id = get_jwt_identity()
        booking = Booking.query.get_or_404(id)
        if booking.user_id != current_user_id:
            api.abort(403, "You don't have permission to access this booking")
        return booking

    @ns.doc('update_booking',
        description='Update a booking',
        security='Bearer'
    )
    @ns.expect(booking_update_model)
    @ns.marshal_with(booking_model)
    @ns.response(403, 'Not authorized to update this booking')
    @ns.response(404, 'Booking not found')
    @jwt_required()
    def put(self, id):
        """Update a booking"""
        current_user_id = get_jwt_identity()
        booking = Booking.query.get_or_404(id)
        
        if booking.user_id != current_user_id:
            api.abort(403, "You don't have permission to update this booking")
        
        data = request.get_json()
        
        if 'start_time' in data:
            booking.start_time = parse_iso_datetime(data['start_time'])
        if 'end_time' in data:
            booking.end_time = parse_iso_datetime(data['end_time'])
        if 'status' in data:
            booking.status = data['status']
        
        db.session.commit()
        return booking

    @ns.doc('delete_booking',
        description='Delete a booking',
        security='Bearer'
    )
    @ns.response(204, 'Booking deleted')
    @ns.response(403, 'Not authorized to delete this booking')
    @ns.response(404, 'Booking not found')
    @jwt_required()
    def delete(self, id):
        """Delete a booking"""
        current_user_id = get_jwt_identity()
        booking = Booking.query.get_or_404(id)
        
        if booking.user_id != current_user_id:
            api.abort(403, "You don't have permission to delete this booking")
        
        db.session.delete(booking)
        db.session.commit()
        return '', 204

@ns.route('/available')
class AvailableWorkspaces(Resource):
    @ns.doc('get_available_workspaces',
        description='Get available workspaces for a time period',
        params={
            'start_time': {'description': 'Start time (ISO 8601 format with UTC timezone)', 'required': True},
            'end_time': {'description': 'End time (ISO 8601 format with UTC timezone)', 'required': True}
        }
    )
    @ns.response(400, 'Invalid input')
    def get(self):
        """Get available workspaces for a time period"""
        start_time = request.args.get('start_time')
        end_time = request.args.get('end_time')
        
        if not start_time or not end_time:
            api.abort(400, "Start time and end time are required")
            
        start_time = parse_iso_datetime(start_time)
        end_time = parse_iso_datetime(end_time)
        
        # Get all workspaces
        workspaces = Workspace.query.filter_by(is_available=True).all()
        
        # Filter out workspaces that have overlapping bookings
        available_workspaces = []
        for workspace in workspaces:
            overlapping = Booking.query.filter(
                Booking.workspace_id == workspace.id,
                Booking.status == 'confirmed',
                ((Booking.start_time <= start_time) & (Booking.end_time > start_time)) |
                ((Booking.start_time < end_time) & (Booking.end_time >= end_time)) |
                ((Booking.start_time >= start_time) & (Booking.end_time <= end_time))
            ).first()
            
            if not overlapping:
                available_workspaces.append(workspace)
                
        return [{'id': ws.id, 'name': ws.name, 'description': ws.description, 'capacity': ws.capacity} 
                for ws in available_workspaces]

@ns.route('/<int:id>/confirm')
@ns.param('id', 'The booking identifier')
class BookingConfirmation(Resource):
    @ns.doc('confirm_booking',
        description='Confirm a pending booking',
        security='Bearer'
    )
    @ns.marshal_with(booking_model)
    @ns.response(400, 'Invalid booking status or overlapping booking')
    @ns.response(403, 'Not authorized to confirm this booking')
    @ns.response(404, 'Booking not found')
    @jwt_required()
    def post(self, id):
        """Confirm a booking"""
        current_user_id = get_jwt_identity()
        booking = Booking.query.get_or_404(id)
        
        if booking.user_id != current_user_id:
            api.abort(403, "You don't have permission to confirm this booking")
            
        if booking.status != 'pending':
            api.abort(400, "Only pending bookings can be confirmed")
            
        # Check if there are any overlapping confirmed bookings
        overlapping = Booking.query.filter(
            Booking.workspace_id == booking.workspace_id,
            Booking.id != booking.id,
            Booking.status == 'confirmed',
            ((Booking.start_time <= booking.start_time) & (Booking.end_time > booking.start_time)) |
            ((Booking.start_time < booking.end_time) & (Booking.end_time >= booking.end_time)) |
            ((Booking.start_time >= booking.start_time) & (Booking.end_time <= booking.end_time))
        ).first()
        
        if overlapping:
            api.abort(400, "There is an overlapping confirmed booking for this workspace")
            
        booking.status = 'confirmed'
        db.session.commit()
        return booking 