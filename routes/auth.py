
from flask import Blueprint, request, jsonify
from models.user import User
from models.token import Token
from extensions import db, bcrypt
import uuid
import jwt
from datetime import datetime, timezone, timedelta
from functools import wraps

SECRET_KEY = "board_game_IS_FUN!!!"

auth_blueprint = Blueprint('auth', __name__)


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        
        if not token:
            return jsonify({"message": "Token is missing"}), 401
        
        parts = token.split()
        if len(parts) != 2 or parts[0].lower() != "bearer":
            return jsonify({"message": "Invalid token format"}), 401
        
        token = parts[1]
        try:
            data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            user_token = Token.query.filter_by(token=token).first()
            
            if not user_token:
                return jsonify({"message": "Token is invalid"}), 401
            
            # Get current time as offset-aware datetime
            current_time = datetime.now(timezone.utc)
            token_expiry = user_token.expiry
            
            # Ensure the expiry time is offset-aware
            if token_expiry.tzinfo is None:
                token_expiry = token_expiry.replace(tzinfo=timezone.utc)
            
            if token_expiry < current_time:
                db.session.delete(user_token)
                db.session.commit()
                return jsonify({"message": "Token expired. Please log in again."}), 401
            
            return f(userId=data["userId"], *args, **kwargs)
        
        except jwt.ExpiredSignatureError:
            return jsonify({"message": "Token expired"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"message": "Token is invalid"}), 401
    
    return decorated


@auth_blueprint.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('userEmail')
    password = data.get('userPassword')

    user = User.query.filter_by(userEmail=email).first()
    if not user or not bcrypt.check_password_hash(user.userPassword, password):
        return jsonify({"message": "Invalid email or password"}), 401

    # Remove old tokens
    Token.query.filter_by(userId=user.userId).delete()
    db.session.commit()

    # Generate a new token
    token = jwt.encode({
        "userId": user.userId,
        "exp": datetime.now(timezone.utc) + timedelta(hours=24)
    }, SECRET_KEY, algorithm="HS256")

    new_token = Token(userId=user.userId, token=token)
    db.session.add(new_token)
    db.session.commit()

    return jsonify({"token": token})


@auth_blueprint.route('/logout', methods=['POST'])
@token_required
def logout():
    token = request.headers.get('Authorization')
    Token.query.filter_by(token=token).delete()
    db.session.commit()
    return jsonify({"message": "Logged out successfully"}), 200
