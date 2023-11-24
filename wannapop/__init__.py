from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from flask_login import LoginManager
from flask_principal import Principal
from .helper_mail import MailManager

db_manager = SQLAlchemy()
login_manager = LoginManager()
principal_manager =  Principal()
mail_manager = MailManager()


def create_app():
    # Construct the core app object
    app = Flask(__name__)

    # Configura la aplicación con la clase Config de config.py
    app.config.from_object("config.Config")
    
    # Inicialitza els plugins
    login_manager.init_app(app)
    db_manager.init_app(app)
    principal_manager.init_app(app)
    mail_manager.init_app(app)

    with app.app_context():
        from . import routes_main, routes_auth, routes_admin

        # Registra els blueprints
        app.register_blueprint(routes_main.main_bp)
        app.register_blueprint(routes_auth.auth_bp)
        app.register_blueprint(routes_admin.admin_bp)

    app.logger.info("Aplicació iniciada")

    return app