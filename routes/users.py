from flask import Blueprint, request, jsonify
from models.user import User
from extensions import db
from flask_bcrypt import Bcrypt
import uuid

user_blueprint = Blueprint('users', __name__)
bcrypt = Bcrypt()

# Register a new user
@user_blueprint.route('/register', methods=['POST'])
def register():
    data = request.json

    if User.query.filter_by(userEmail=data['userEmail']).first():
        return jsonify({'error': 'Email already registered'}), 400

    user_id = str(uuid.uuid4())
    hashed_password = bcrypt.generate_password_hash(data['userPassword']).decode('utf-8')

    new_user = User(
        userId=user_id,
        userName=data['userName'],
        userEmail=data['userEmail'],
        userPassword=hashed_password
    )

    try:
        db.session.add(new_user)
        db.session.commit()
        return jsonify({'message': 'User registered successfully!', 'userId': user_id}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# Login a user
@user_blueprint.route('/login', methods=['POST'])
def login():
    data = request.json

    user = User.query.filter_by(userEmail=data['userEmail']).first()

    if user and bcrypt.check_password_hash(user.userPassword, data['userPassword']):
        return jsonify({
            'message': 'Login successful!',
            'userId': user.userId,
            'userName': user.userName,
            'userEmail': user.userEmail
        }), 200
    else:
        return jsonify({'error': 'Invalid email or password'}), 401

# Get user profile
@user_blueprint.route('/profile/<userId>', methods=['GET'])
def get_user_profile(userId):
    user = User.query.filter_by(userId=userId).first()
    if user:
        return jsonify({
            'userId': user.userId,
            'userName': user.userName,
            'userEmail': user.userEmail,
            'userStatus': user.userStatus,
            'userProfileDescription': user.userProfileDescription,
            'userLevel': user.userLevel,
            'userTotalScore': user.userTotalScore,
            'userCoins': user.userCoins,
            'userStats': user.userStats,
            'userActivity': user.userActivity
        }), 200
    else:
        return jsonify({'error': 'User not found'}), 404

# Update user profile
@user_blueprint.route('/profile/<userId>', methods=['PUT'])
def update_user_profile(userId):
    data = request.json
    user = User.query.filter_by(userId=userId).first()

    if user:
        try:
            user.userName = data.get('userName', user.userName)
            user.userProfileDescription = data.get('userProfileDescription', user.userProfileDescription)
            user.userLevel = data.get('userLevel', user.userLevel)
            user.userTotalScore = data.get('userTotalScore', user.userTotalScore)
            user.userCoins = data.get('userCoins', user.userCoins)
            user.userStats = data.get('userStats', user.userStats)
            user.userActivity = data.get('userActivity', user.userActivity)

            db.session.commit()
            return jsonify({'message': 'User profile updated successfully!'}), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500
    else:
        return jsonify({'error': 'User not found'}), 404
