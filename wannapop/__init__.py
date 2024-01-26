from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from flask_login import LoginManager
from flask_principal import Principal
from .helper_mail import MailManager
from werkzeug.local import LocalProxy
from flask import current_app
from flask_debugtoolbar import DebugToolbarExtension
from logging.handlers import RotatingFileHandler
import logging

# https://stackoverflow.com/a/31764294
logger = LocalProxy(lambda: current_app.logger)

db_manager = SQLAlchemy()
login_manager = LoginManager()
principal_manager =  Principal()
mail_manager = MailManager()
toolbar = DebugToolbarExtension()


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
    toolbar.init_app(app) # the toolbar is only enabled in debug mode

    #gestion de logs
    log_handler = RotatingFileHandler('app.log', maxBytes=10240, backupCount=3)
    log_handler.setFormatter(logging.Formatter(
   '%(asctime)s %(levelname)s: %(message)s '
   '[in %(pathname)s:%(lineno)d]'
    ))
    log_handler.setLevel(logging.DEBUG)
    app.logger.addHandler(log_handler)

    

    log_level = app.config.get('LOG_LEVEL')
    if log_level not in ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']:
        raise ValueError('Nivell de registre no vàlid')
    app.logger.setLevel(getattr(logging, log_level))



    with app.app_context():
        from . import routes_main, routes_auth, routes_admin
        from .api import api_bp

        # Registra els blueprints
        app.register_blueprint(routes_main.main_bp)
        app.register_blueprint(routes_auth.auth_bp)
        app.register_blueprint(routes_admin.admin_bp)
        # Registra el blueprint de l'API
        app.register_blueprint(api_bp, url_prefix='/api/v1.0')

    app.logger.info("Aplicació iniciada")

    return app