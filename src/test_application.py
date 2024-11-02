# test_application.py

import pytest
from src.application import app, mongo
from flask import session

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['MONGO_URI'] = 'mongodb://localhost:27017/simplii_test'  
    with app.test_client() as client:
        with app.app_context():
            mongo.db.users.drop()  
            mongo.db.tasks.drop()
        yield client

def test_home_redirects_to_login(client):
    response = client.get('/')
    assert response.status_code == 302
    assert response.headers['Location'].endswith('/login')

def test_register_user(client):
    response = client.post('/register', data={
        'username': 'testuser',
        'email': 'test@example.com',
        'password': 'password123'
    })
    assert b'OTP sent to test@example.com' in response.data
    user = mongo.db.users.find_one({'email': 'test@example.com'})
    assert user is not None

def test_otp_verification(client):
    client.post('/register', data={
        'username': 'testuser',
        'email': 'test@example.com',
        'password': 'password123'
    })
    user = mongo.db.users.find_one({'email': 'test@example.com'})
    otp = user['otp']
    response = client.post('/otp_verification', data={'otp': otp})
    assert b'Your account has been verified successfully!' in response.data

def test_login_user(client):
    # Register and verify user
    client.post('/register', data={
        'username': 'testuser',
        'email': 'test@example.com',
        'password': 'password123'
    })
    user = mongo.db.users.find_one({'email': 'test@example.com'})
    mongo.db.users.update_one({'email': 'test@example.com'}, {'$set': {'is_verified': True}})

    # Login
    response = client.post('/login', data={'email': 'test@example.com', 'password': 'password123'})
    assert response.status_code == 302  # Redirect after login
    assert response.headers['Location'].endswith('/dashboard')

def test_dashboard_access(client):
    # Access dashboard without login
    response = client.get('/dashboard')
    assert response.status_code == 302  # Redirect to login

def test_task_creation(client):
    client.post('/register', data={
        'username': 'testuser',
        'email': 'test@example.com',
        'password': 'password123'
    })
    client.post('/login', data={'email': 'test@example.com', 'password': 'password123'})

    response = client.post('/task', data={
        'taskname': 'Test Task',
        'category': 'Work',
        'startdate': '2024-11-01',
        'duedate': '2024-11-05',
        'status': 'To-Do',
        'hours': 5
    })
    assert b'Task Added!' in response.data
    task = mongo.db.tasks.find_one({'taskname': 'Test Task'})
    assert task is not None

def test_email_reminder(client):
    client.post('/register', data={
        'username': 'testuser',
        'email': 'test@example.com',
        'password': 'password123'
    })
    client.post('/login', data={'email': 'test@example.com', 'password': 'password123'})

    response = client.post('/send_email_reminders', data={'duedate': '2024-11-10'})
    assert b'Email reminders sent' in response.data

def test_task_edit(client):
    client.post('/register', data={
        'username': 'testuser',
        'email': 'test@example.com',
        'password': 'password123'
    })
    client.post('/login', data={'email': 'test@example.com', 'password': 'password123'})

    client.post('/task', data={
        'taskname': 'Initial Task',
        'category': 'Work',
        'startdate': '2024-11-01',
        'duedate': '2024-11-05',
        'status': 'To-Do',
        'hours': 5
    })
    
    response = client.post('/editTask', data={
        'taskname': 'Updated Task',
        'category': 'Updated',
        'startdate': '2024-11-02',
        'duedate': '2024-11-06',
        'status': 'In Progress',
        'hours': 6
    })
    assert b'Task Updated!' in response.data

def test_delete_task(client):
    client.post('/register', data={
        'username': 'testuser',
        'email': 'test@example.com',
        'password': 'password123'
    })
    client.post('/login', data={'email': 'test@example.com', 'password': 'password123'})

    client.post('/task', data={
        'taskname': 'Task to Delete',
        'category': 'Work',
        'startdate': '2024-11-01',
        'duedate': '2024-11-05',
        'status': 'To-Do',
        'hours': 5
    })
    response = client.post('/deleteTask', data={'task': 'Task to Delete', 'status': 'To-Do', 'category': 'Work'})
    assert response.data == b'Success'

def test_chatbot_valid_input(client, mocker):
    mock_response = mocker.Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        'candidates': [{'content': {'parts': [{'text': 'Sample response from chatbot'}]}}]
    }
    mocker.patch('requests.post', return_value=mock_response)

    response = client.post('/chatbot', data={'user_input': 'What is AI?'})
    assert response.status_code == 200
    assert b'Sample response from chatbot' in response.data

def test_chatbot_empty_input(client):
    response = client.post('/chatbot', data={'user_input': ''})
    assert b'Failed to fetch response from Gemini API.' not in response.data
    assert response.status_code == 200  # Should still return the chatbot HTML

def test_chatbot_error_from_api(client, mocker):
    mock_response = mocker.Mock()
    mock_response.status_code = 500
    mocker.patch('requests.post', return_value=mock_response)

    response = client.post('/chatbot', data={'user_input': 'Explain AI ethics'})
    assert response.status_code == 500
    assert b'Failed to fetch response from Gemini API.' in response.data

def test_chatbot_invalid_method(client):
    # Test GET request to chatbot instead of POST
    response = client.get('/chatbot')
    assert response.status_code == 200  # Should return the chatbot HTML page for GET

def test_chatbot_missing_key(client, mocker):
    mock_response = mocker.Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {}
    mocker.patch('requests.post', return_value=mock_response)

    response = client.post('/chatbot', data={'user_input': 'What is deep learning?'})
    assert response.status_code == 500  # Should return a server error if the API response is missing data
    assert b'Failed to fetch response from Gemini API.' in response.data
