# models/stats.py
from extensions import db

class Stats(db.Model):
    __tablename__ = 'stats'
    statsId = db.Column(db.Integer, primary_key=True)
    totalGamesPlayed = db.Column(db.Integer, default=0, nullable=False)
    totalWins = db.Column(db.Integer, default=0, nullable=False)
    totalLosses = db.Column(db.Integer, default=0, nullable=False)
    rankScore = db.Column(db.Integer, default=0, nullable=False)
    userId = db.Column(db.String(36), db.ForeignKey('users.userId'), nullable=False)