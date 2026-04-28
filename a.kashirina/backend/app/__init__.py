from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt
from config import Config

# Initialize extensions
db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()
bcrypt = Bcrypt()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    bcrypt.init_app(app)
    
    # CORS
    CORS(app, resources={
        r"/*": {
            "origins": app.config['CORS_ORIGINS'],
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": app.config['CORS_HEADERS'],
            "supports_credentials": app.config['CORS_SUPPORTS_CREDENTIALS']
        }
    })

    # blueprints
    from app.api import bp as api_bp
    app.register_blueprint(api_bp, url_prefix='/api')

    # error handlers
    from app.errors import bp as errors_bp
    app.register_blueprint(errors_bp)

    from app import models

    return app