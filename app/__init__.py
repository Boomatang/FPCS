from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import config

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.session_protection = 'strong'



def create_app(config_name):
    """
    factory funtion to create the app. I do not fully understand what is goin on here
    """
    app = Flask(__name__)
    
    app.config.from_object(config[config_name])
    
    config[config_name].init_app(app)
    db.init_app(app)
    
    return app
