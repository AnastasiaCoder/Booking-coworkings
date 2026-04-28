import pytest
from app import create_app, db
from app.models import User, Workspace, Booking
from datetime import datetime, timedelta
from config import TestConfig

@pytest.fixture
def app():
    app = create_app(TestConfig)
    
    with app.app_context():
        # Существуют ли таблицы
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def test_user(app):
    user = User(first_name='newuser', email='new@example.com')
    user.set_password('password')
    db.session.add(user)
    db.session.commit()
    
    assert user.check_password('password'), "Password was not hashed correctly"
    return user

@pytest.fixture
def auth_headers(test_user, client):
    # Получить токен
    response = client.post('/api/auth/login', json={
        'email': 'new@example.com',
        'password': 'password'
    })
    assert response.status_code == 200, f"Login failed: {response.get_data(as_text=True)}"
    assert 'access_token' in response.json, f"Response missing access_token: {response.json}"
    token = response.json['access_token']
    return {'Authorization': f'Bearer {token}'}

@pytest.fixture
def test_workspace(app):
    # Создание рабочего места
    workspace = Workspace(
        name='Test Workspace', 
        description='Test Description', 
        capacity=1,
        price_per_hour=50.0
    )
    db.session.add(workspace)
    db.session.commit()
    return workspace

def test_create_user(client):
    # Создать пользователя с хешированным паролем
    user = User(first_name='newuser', email='new@example.com')
    user.set_password('password')
    
    response = client.post('/api/users/', json={
        'first_name': 'newuser',
        'email': 'new@example.com',
        'password': 'password'
    })
    assert response.status_code == 201
    assert response.json['first_name'] == 'newuser'
    assert response.json['email'] == 'new@example.com'

def test_create_workspace(client, auth_headers):
    # Создание рабочего места
    response = client.post('/api/workspaces/', 
        json={
            'name': 'New Workspace',
            'description': 'New Description',
            'capacity': 2,
            'price_per_hour': 100.0
        },
        headers=auth_headers
    )
    assert response.status_code == 201
    assert response.json['name'] == 'New Workspace'
    assert response.json['capacity'] == 2
    assert response.json['price_per_hour'] == 100.0

def test_create_booking(client, test_user, test_workspace, auth_headers):
    start_time = datetime.utcnow() + timedelta(hours=1)
    end_time = start_time + timedelta(hours=2)
    
    response = client.post('/api/bookings/', 
        json={
            'user_id': test_user.id,
            'workspace_id': test_workspace.id,
            'start_time': start_time.isoformat(),
            'end_time': end_time.isoformat()
        },
        headers=auth_headers
    )
    assert response.status_code == 201
    assert response.json['user_id'] == test_user.id
    assert response.json['workspace_id'] == test_workspace.id

def test_get_available_workspaces(client, test_workspace, auth_headers):
    start_time = datetime.utcnow() + timedelta(hours=1)
    end_time = start_time + timedelta(hours=2)
    
    response = client.get(
        f'/api/bookings/available?start_time={start_time.isoformat()}&end_time={end_time.isoformat()}',
        headers=auth_headers
    )
    assert response.status_code == 200
    assert len(response.json) == 1
    assert response.json[0]['id'] == test_workspace.id 