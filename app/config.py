import os

SECRET_KEY = 'your-secret-key'
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(os.path.dirname(__file__), 'data.db')
SQLALCHEMY_TRACK_MODIFICATIONS = False
JWT_SECRET_KEY = 'your-jwt-secret-key'
