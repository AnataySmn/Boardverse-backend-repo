from flask_sqlalchemy import SQLAlchemy
from extensions import db

class User(db.Model):
    __tablename__ = 'user_profiles'

    userId = db.Column(db.String(36), primary_key=True)
    userName = db.Column(db.String(255), nullable=False)
    userEmail = db.Column(db.String(255), unique=True, nullable=False)
    userPassword = db.Column(db.String(255), nullable=False)
    userStatus = db.Column(db.String(50), default='Away', nullable=False)
    userProfileDescription = db.Column(db.Text, nullable=True)
    userProfilePic = db.Column(db.LargeBinary, nullable=True)
    userLevel = db.Column(db.Integer, default=1, nullable=False)
    userTotalScore = db.Column(db.Integer, default=0, nullable=False)
    userCoins = db.Column(db.Integer, default=100, nullable=False)
    userStats = db.Column(db.JSON, nullable=True)
    userActivity = db.Column(db.JSON, nullable=True)
