import os
from dotenv import load_dotenv
from datetime import timedelta

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'postgresql://postgres:postgres@db:5432/coworking'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'jwt-secret-key'
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    CORS_HEADERS = ['Content-Type', 'Authorization']
    CORS_ORIGINS = ['http://localhost:3000']
    CORS_SUPPORTS_CREDENTIALS = True
    
    # Bcrypt
    BCRYPT_LOG_ROUNDS = 12
    BCRYPT_HASH_PREFIX = '2b'

class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:postgres@db/coworking_test'
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False 