from extensions import db

class User(db.Model):
    __tablename__ = 'users'
    userId = db.Column(db.String(36), primary_key=True)
    userName = db.Column(db.String(255), nullable=False)
    userEmail = db.Column(db.String(255), unique=True, nullable=False)
    userPassword = db.Column(db.String(255), nullable=False)
    userStatus = db.Column(db.String(50), default='Away', nullable=False)
    userProfileDescription = db.Column(db.Text, nullable=True)
    userProfilePic = db.Column(db.LargeBinary, nullable=True)
    userLevel = db.Column(db.Integer, default=1, nullable=False)
    userCoins = db.Column(db.Integer, default=100, nullable=False)

    stats = db.relationship('Stats', backref='user', uselist=False, cascade="all, delete-orphan")
    activities = db.relationship('Activity', backref='user', cascade="all, delete-orphan")
