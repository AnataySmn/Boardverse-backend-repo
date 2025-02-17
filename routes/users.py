from flask import Blueprint, request, jsonify
from models.user import User
from models.stats import Stats
from models.activity import Activity
from extensions import db, bcrypt
import uuid
from routes.auth import token_required


user_blueprint = Blueprint('users', __name__)

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
        # Add user to the database
        db.session.add(new_user)
        db.session.flush()  # Ensure the user is committed before adding related entries

        # Automatically create stats and activity for the user
        new_stats = Stats(userId=user_id, statsId=str(uuid.uuid4()))
        db.session.add(new_stats)

        db.session.commit()
        return jsonify({'message': 'User registered successfully!', 'userId': user_id}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# Get user profile
@user_blueprint.route('/profile', methods=['GET'])
@token_required
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
            'userCoins': user.userCoins
        }), 200
    else:
        return jsonify({'error': 'User not found'}), 404

# Update user profile
@user_blueprint.route('/profile', methods=['PUT'])
@token_required
def update_user_profile(userId):
    data = request.json
    user = User.query.filter_by(userId=userId).first()

    if user:
        try:
            user.userName = data.get('userName', user.userName)
            user.userProfileDescription = data.get('userProfileDescription', user.userProfileDescription)
            user.userLevel = data.get('userLevel', user.userLevel)
            user.userCoins = data.get('userCoins', user.userCoins)

            db.session.commit()
            return jsonify({'message': 'User profile updated successfully!'}), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500
    else:
        return jsonify({'error': 'User not found'}), 404
