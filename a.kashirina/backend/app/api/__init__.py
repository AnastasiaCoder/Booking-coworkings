from flask import Blueprint
from flask_restx import Api

# blueprint
bp = Blueprint('api', __name__)

# API instance
api = Api(bp,
    title='Coworking Space API',
    version='1.0',
    description='API for managing coworking space bookings and workspaces',
    doc='/docs',
    authorizations={
        'Bearer': {
            'type': 'apiKey',
            'in': 'header',
            'name': 'Authorization',
            'description': 'Type in the *\'Value\'* input box below: **\'Bearer &lt;JWT&gt;\'**, where JWT is the token'
        }
    },
    security='Bearer'
)

# Import namespaces
from app.api.bookings import ns as bookings_ns
from app.api.workspaces import ns as workspaces_ns
from app.api.auth import ns as auth_ns

# Add namespaces to API
api.add_namespace(auth_ns, path='/api/auth')
api.add_namespace(bookings_ns, path='/api/bookings')
api.add_namespace(workspaces_ns, path='/api/workspaces')

def init_app(app):
    """Initialize the API with the app"""
    api.init_app(app)
    
    # namespaces
    from app.api.bookings import ns as bookings_ns
    from app.api.workspaces import ns as workspaces_ns
    from app.api.auth import ns as auth_ns

    # Add namespaces to API
    api.add_namespace(auth_ns, path='/api/auth')
    api.add_namespace(bookings_ns, path='/api/bookings')
    api.add_namespace(workspaces_ns, path='/api/workspaces')

# Импортируем после создания api
from app.api import auth, users, workspaces, bookings 