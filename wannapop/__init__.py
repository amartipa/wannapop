from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from config import Config
from flask_login import LoginManager
from flask_principal import Principal

db_manager = SQLAlchemy()
login_manager = LoginManager()
principal_manager =  Principal()



def create_app():
    # Construct the core app object
    app = Flask(__name__)

    # Configura la aplicación con la clase Config de config.py
    app.config.from_object(Config)
    
    # Inicialitza els plugins
    login_manager.init_app(app)
    db_manager.init_app(app)
    principal_manager.init_app(app)

    with app.app_context():
        from . import routes_main, routes_auth, routes_admin

        # Registra els blueprints
        app.register_blueprint(routes_main.main_bp)
        app.register_blueprint(routes_auth.auth_bp)
        app.register_blueprint(routes_admin.admin_bp)

    app.logger.info("Aplicació iniciada")

    return app