from datetime import datetime, timedelta, timezone
import uuid
from extensions import db



class Token(db.Model):
    __tablename__ = 'tokens'

    tokenId = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    userId = db.Column(db.String(36), db.ForeignKey('users.userId'), nullable=False)
    token = db.Column(db.String(512), nullable=False, unique=True)
    expiry = db.Column(db.DateTime, nullable=False)

    def __init__(self, userId, token):
        self.userId = userId
        self.token = token
        self.expiry = datetime.now(timezone.utc) + timedelta(hours=24)  # Token valid for 1 hour
