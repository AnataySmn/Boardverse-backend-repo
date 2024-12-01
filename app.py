import os
from dotenv import load_dotenv
from flask import Flask
from flask_bcrypt import Bcrypt
from extensions import db
from routes.users import user_blueprint

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Configure the database
db_uri = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize extensions
db.init_app(app)
bcrypt = Bcrypt(app)

# Register blueprints
app.register_blueprint(user_blueprint, url_prefix='/user')

# Create database tables (for development)
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
