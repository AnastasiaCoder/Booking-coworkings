"""add seed data

Revision ID: c2f911a39085
Revises: f601347b5e57
Create Date: 2025-05-10 19:34:11.000000

"""
from alembic import op
import sqlalchemy as sa
from app import bcrypt
from datetime import datetime
from config import Config
from flask import Flask

revision = 'c2f911a39085'
down_revision = 'f601347b5e57'
branch_labels = None
depends_on = None


def upgrade():
    temp_app = Flask(__name__)
    temp_app.config.from_object(Config)
    bcrypt.init_app(temp_app)
    
    password = 'password'
    hash1 = bcrypt.generate_password_hash(password).decode('utf-8')
    hash2 = bcrypt.generate_password_hash(password).decode('utf-8')
    
    print(f"Hash 1: {hash1}")
    print(f"Hash 2: {hash2}")
    
    print(f"Hash 1 verifies: {bcrypt.check_password_hash(hash1, password)}")
    print(f"Hash 2 verifies: {bcrypt.check_password_hash(hash2, password)}")
    
    password_hash = hash1
    
    users_table = sa.table('users',
        sa.column('email', sa.String),
        sa.column('password_hash', sa.String),
        sa.column('first_name', sa.String),
        sa.column('last_name', sa.String),
        sa.column('created_at', sa.DateTime)
    )
    op.bulk_insert(users_table, [
        {
            'email': 'person@example.com',
            'password_hash': bcrypt.generate_password_hash('admin123').decode('utf-8'),
            'first_name': 'Persona',
            'last_name': 'User',
            'created_at': datetime.utcnow()
        },
        {
            'email': 'user@example.com',
            'password_hash': bcrypt.generate_password_hash('user123').decode('utf-8'),
            'first_name': 'Regular',
            'last_name': 'User',
            'created_at': datetime.utcnow()
        }
    ])

    workspaces_table = sa.table('workspaces',
        sa.column('name', sa.String),
        sa.column('description', sa.Text),
        sa.column('capacity', sa.Integer),
        sa.column('price_per_hour', sa.Float),
        sa.column('is_available', sa.Boolean),
        sa.column('created_at', sa.DateTime)
    )
    op.bulk_insert(workspaces_table, [
        {
            'name': 'Рабочее место №1',
            'description': 'Удобное рабочее место с компьютером и доступом к интернету(на ремонте)',
            'capacity': 1,
            'price_per_hour': 500.0,
            'is_available': False,
            'created_at': datetime.utcnow()
        },
        {
            'name': 'Рабочее место №2',
            'description': 'Тихое рабочее место для индивидуальной работы',
            'capacity': 1,
            'price_per_hour': 450.0,
            'is_available': True,
            'created_at': datetime.utcnow()
        },
        {
            'name': 'Конференц-зал',
            'description': 'Просторный зал для проведения встреч и презентаций',
            'capacity': 10,
            'price_per_hour': 2000.0,
            'is_available': True,
            'created_at': datetime.utcnow()
        },
        {
            'name': 'Переговорная комната',
            'description': 'Небольшая комната для командных встреч',
            'capacity': 4,
            'price_per_hour': 1000.0,
            'is_available': True,
            'created_at': datetime.utcnow()
        }
    ])


def downgrade():
    op.execute(
        """
        DELETE FROM users WHERE email = 'user@example.com'
        """
    )

