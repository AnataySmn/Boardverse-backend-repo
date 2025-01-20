from flask_sqlalchemy import SQLAlchemy

#initialized here so the same instance can be used across all models, routes and stuff  
db = SQLAlchemy()
