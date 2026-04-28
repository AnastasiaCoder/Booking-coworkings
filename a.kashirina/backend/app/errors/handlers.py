from flask import jsonify
from werkzeug.http import HTTP_STATUS_CODES
from app.errors import bp
from flask_jwt_extended import JWTManager
from app import jwt

def error_response(status_code, message=None):
    payload = {'error': HTTP_STATUS_CODES.get(status_code, 'Unknown error')}
    if message:
        payload['message'] = message
    response = jsonify(payload)
    response.status_code = status_code
    return response

@bp.app_errorhandler(400)
def bad_request(error):
    return error_response(400)

@bp.app_errorhandler(401)
def unauthorized(error):
    return error_response(401)

@bp.app_errorhandler(403)
def forbidden(error):
    return error_response(403)

@bp.app_errorhandler(404)
def not_found(error):
    return error_response(404)

@bp.app_errorhandler(500)
def internal_server_error(error):
    return error_response(500)

@jwt.expired_token_loader
def expired_token_callback(jwt_header, jwt_payload):
    return jsonify({
        'message': 'The token has expired',
        'error': 'token_expired'
    }), 401

@jwt.invalid_token_loader
def invalid_token_callback(error):
    return jsonify({
        'message': 'Invalid token',
        'error': 'invalid_token'
    }), 401

@jwt.unauthorized_loader
def unauthorized_callback(error):
    return jsonify({
        'message': 'Missing authorization header',
        'error': 'authorization_required'
    }), 401 