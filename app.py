import os
from dotenv import load_dotenv
from flask import Flask
from extensions import db, bcrypt
from flask_cors import CORS

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Enable CORS
CORS(app, resources={r"/*": {"origins": "*", "methods": ["GET", "POST", "PUT", "DELETE"]}})

# Configure the database
db_uri = os.getenv('DATABASE_URL', 'sqlite:///boardverse.db')  
app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize extensions
db.init_app(app)
bcrypt.init_app(app)

from routes.users import user_blueprint
from routes.stats import stats_blueprint
from routes.activities import activity_blueprint
from routes.auth import auth_blueprint

# Register blueprints
app.register_blueprint(user_blueprint, url_prefix='/user')
app.register_blueprint(stats_blueprint, url_prefix='/stats')
app.register_blueprint(activity_blueprint, url_prefix='/activities')
app.register_blueprint(auth_blueprint, url_prefix='/auth')

# Create database tables
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
