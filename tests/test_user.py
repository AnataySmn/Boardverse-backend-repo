import pytest
from app import app
from extensions import db  # Use the shared SQLAlchemy instance
from models.user import User
from flask_bcrypt import Bcrypt
import random
 
# Initialize Flask Bcrypt
bcrypt = Bcrypt()
 
# Fixture to configure the app for testing and setup the database
@pytest.fixture
def client():
    # Override app configuration for testing
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'  # Use a test SQLite database
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
 
    # Safety check: Ensure the database URI is for testing
    if not app.config['SQLALCHEMY_DATABASE_URI'].endswith('test.db'):
        raise RuntimeError("Tests must run on the test database!")
 
    # Initialize the test client and database
    with app.test_client() as client:
        with app.app_context():
            db.create_all()  # Create tables for the test database
        yield client
        # Cleanup: Clear data from all tables after each test
        with app.app_context():
            for table in reversed(db.metadata.sorted_tables):
                db.session.execute(table.delete())  # Delete all rows
            db.session.commit()
 
# Helper function to create a test user
def create_test_user():
    return User(
        userId=f"test-id-{random.randint(1, 10000)}",  # Generate a unique userId
        userName="Test User",
        userEmail="test@example.com",
        userPassword=bcrypt.generate_password_hash("password123").decode('utf-8')
    )
 
# TEST CASE 1: Register a new user
def test_register_user(client):
    response = client.post('/user/register', json={
        'userName': 'Billy Miligan',
        'userEmail': 'billym@example.com',
        'userPassword': 'mypassword'
    })
    assert response.status_code == 201
 
    with app.app_context():
        user = User.query.filter_by(userEmail='billym@example.com').first()
        assert user is not None
        assert user.userName == 'Billy Miligan'
        assert user.userEmail == 'billym@example.com'
 
# TEST CASE 2: Login with valid credentials
def test_login_user(client):
    test_user = create_test_user()
    with app.app_context():
        db.session.add(test_user)
        db.session.commit()
 
    response = client.post('/user/login', json={
        'userEmail': 'test@example.com',
        'userPassword': 'password123'
    })
    assert response.status_code == 200
    data = response.get_json()
    assert data['message'] == 'Login successful!'
    assert data['userName'] == 'Test User'
    assert data['userEmail'] == 'test@example.com'
 
# TEST CASE 3: Update user profile
def test_update_user_profile(client):
    test_user = create_test_user()
    with app.app_context():
        db.session.add(test_user)
        db.session.commit()
        
        # Re-query the user from the database
        test_user = User.query.filter_by(userId=test_user.userId).first()
        
        # Perform the PUT request
        response = client.put(f'/user/profile/{test_user.userId}', json={
            'userName': 'Updated User',
            'userProfileDescription': 'This is a test profile.'
        })
        
        # Assertions
        assert response.status_code == 200
        updated_user = User.query.filter_by(userId=test_user.userId).first()
        assert updated_user.userName == 'Updated User'
        assert updated_user.userProfileDescription == 'This is a test profile.'
 
