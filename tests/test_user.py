import pytest
from app import app 
from extensions import db
from models.user import User    
from flask_bcrypt import Bcrypt
import json

bcrypt = Bcrypt()

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # In-memory SQLite for testing
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    with app.test_client() as client:
        with app.app_context():
            db.create_all()  # Create all tables for the test database
        yield client
        with app.app_context():
            db.session.remove()
            db.drop_all()  # Drop all tables after tests


def create_test_user():
    """Function to create a test user."""
    return User(
        userId="test-id",
        userName="Test User",
        userEmail="test@example.com",
        userPassword=bcrypt.generate_password_hash("password123").decode('utf-8')
    )
    
    # Test Case 1: Register a new user
def test_register_user(client):
    response = client.post('/user/register', json={
        'userName': 'Billy Miligan',
        'userEmail': 'billym@example.com',
        'userPassword': 'mypassword'
    })
    assert response.status_code == 201
    data = response.get_json()
    assert data['message'] == 'User registered successfully!'
    assert 'userId' in data
    
    # Test Case 2: Login with valid credentials
def test_login_user(client):
    # Add a test user to the database
    test_user = create_test_user()
    with app.app_context():
        db.session.add(test_user)
        db.session.commit()

    # Login with correct credentials
    response = client.post('/user/login', json={
        'userEmail': 'test@example.com',
        'userPassword': 'password123'
    })
    assert response.status_code == 200
    data = response.get_json()
    assert data['message'] == 'Login successful!'
    assert data['userName'] == 'Test User'
    assert data['userEmail'] == 'test@example.com'
    
    # Test Case 3: Update user profile
def test_update_user_profile(client):
    # Add a test user to the database
    test_user = create_test_user()
    with app.app_context():
        db.session.add(test_user)
        db.session.commit()

        # Retrieve the user again to ensure it's bound to the session
        test_user = User.query.filter_by(userId=test_user.userId).first()

    # Update the user's profile
    response = client.put(f'/user/profile/{test_user.userId}', json={
        'userName': 'Updated User',
        'userProfileDescription': 'This is a test profile.'
    })
    assert response.status_code == 200
    data = response.get_json()
    assert data['message'] == 'User profile updated successfully!'

    # Verify updates in the database
    with app.app_context():
        updated_user = User.query.filter_by(userId=test_user.userId).first()
        assert updated_user.userName == 'Updated User'
        assert updated_user.userProfileDescription == 'This is a test profile.'
    
    
