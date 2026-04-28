from flask import Blueprint, jsonify

bp = Blueprint('errors', __name__)

@bp.app_errorhandler(404)
def not_found_error(error):
    return jsonify({'error': 'Not found'}), 404

@bp.app_errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

@bp.app_errorhandler(400)
def bad_request_error(error):
    return jsonify({'error': 'Bad request'}), 400

@bp.app_errorhandler(401)
def unauthorized_error(error):
    return jsonify({'error': 'Unauthorized'}), 401

@bp.app_errorhandler(403)
def forbidden_error(error):
    return jsonify({'error': 'Forbidden'}), 403

from app.errors import handlers 