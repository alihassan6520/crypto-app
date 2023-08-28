from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from config import Config
import os
db = SQLAlchemy()
jwt = JWTManager()

# import sys
# sys.path.append('/home/sniper/Desktop/hobby/zaply/app')  # Update with the correct path to the 'app' folder


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.py')

    db.init_app(app)
    jwt.init_app(app)

    from app.routes import auth_bp
    app.register_blueprint(auth_bp)

    from app.routes import api_bp
    app.register_blueprint(api_bp)

    return app