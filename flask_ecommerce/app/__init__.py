from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from dotenv import load_dotenv

import os

load_dotenv()

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'main.login'
login_manager.login_message_category = 'main.info'


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'a3b2982747adc10122e5041b7acb9ab8')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    from app import routes 
    bcrypt.init_app(app)
    login_manager.init_app(app)

    from app import routes
    # Import and register your routes
    from .routes import main
    app.register_blueprint(main)

    return app
