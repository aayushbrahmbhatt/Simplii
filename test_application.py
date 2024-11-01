import pytest
from flask import session
from app import app, mongo 

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        with app.app_context():
            mongo.db.users.drop()  
        yield client

def test_home_redirects_to_login(client):
    response = client.get('/')
    assert response.status_code == 302
    assert response.headers['Location'] == '/login'

def test_register_page(client):
    response = client.get('/register')
    assert response.status_code == 200
    assert b'Register' in response.data

def test_login_page(client):
    response = client.get('/login')
    assert response.status_code == 200
    assert b'Login' in response.data

def test_valid_registration(client):
    response = client.post('/register', data={
        'username': 'testuser',
        'email': 'test@example.com',
        'password': 'password123'
    })
    assert b'OTP sent to' in response.data

def test_invalid_login(client):
    response = client.post('/login', data={
        'email': 'wrong@example.com',
        'password': 'wrongpassword'
    })
    assert b'Login Unsuccessful' in response.data

def test_otp_verification(client):
    client.post('/register', data={
        'username': 'testuser',
        'email': 'test@example.com',
        'password': 'password123'
    })
    user = mongo.db.users.find_one({'email': 'test@example.com'})
    otp = user['otp']
    response = client.post('/otp_verification', data={'otp': otp})
    assert b'Your account has been verified successfully' in response.data

def test_dashboard_access(client):
    response = client.get('/dashboard')
    assert response.status_code == 302
    assert response.headers['Location'] == '/login'

def test_task_creation(client):
    client.post('/login', data={
        'email': 'test@example.com',
        'password': 'password123'
    })
    response = client.post('/task', data={
        'taskname': 'Test Task',
        'category': 'Test Category',
        'startdate': '2024-11-01',
        'duedate': '2024-11-05',
        'status': 'To-Do',
        'hours': 5
    })
    assert b'Test Task' in response.data

def test_task_removal(client):
    client.post('/task', data={
        'taskname': 'Test Task',
        'category': 'Test Category',
        'startdate': '2024-11-01',
        'duedate': '2024-11-05',
        'status': 'To-Do',
        'hours': 5
    })
    response = client.post('/deleteTask', data={
        'task': 'Test Task',
        'status': 'To-Do',
        'category': 'Test Category'
    })
    assert response.data == b'Success'

def test_logout(client):
    client.post('/login', data={
        'email': 'test@example.com',
        'password': 'password123'
    })
    response = client.get('/logout')
    assert response.data == b'success'
