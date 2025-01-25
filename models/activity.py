from extensions import db
from datetime import datetime

class Activity(db.Model):
    __tablename__ = 'activities'
    activityId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    gameName = db.Column(db.String(255), nullable=False)
    duration = db.Column(db.Integer, nullable=False)
    result = db.Column(db.String(50), nullable=False)
    rankChange = db.Column(db.Integer, nullable=False)
    playedAt = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    userId = db.Column(db.String(36), db.ForeignKey('users.userId'), nullable=False)