from os import environ, path
import os
from dotenv import load_dotenv

basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '.env'))

class Config:
    """Base config."""
    SECRET_KEY = environ.get('SECRET_KEY')
    # SQLALCHEMY_DATABASE_URI = "sqlite:///" + path.join(basedir, environ.get('SQLITE_FILE_RELATIVE_PATH'))
    # EL POSTGRESSQL FUNCIONA CORRECTAMENTE, LO DEJO COMENTADO YA QUE ES LA RAMA CONJUNTA
    # SQLALCHEMY_DATABASE_URI = "postgresql://2dd12:HHrryn98BHBHMj1x@37.27.3.70:5432/2dd12_pg"
    SQLALCHEMY_DATABASE_URI = environ.get('SQLALCHEMY_DATABASE_URI')
    IMAGES_UPLOAD_PATH = environ.get('IMAGES_UPLOAD_PATH')  # Asegúrate de que esta variable está en tu archivo .env 

    UPLOADS_FOLDER = os.path.join(basedir, IMAGES_UPLOAD_PATH)


    MAIL_SENDER_NAME = environ.get('MAIL_SENDER_NAME')
    MAIL_SENDER_ADDR = environ.get('MAIL_SENDER_ADDR')
    MAIL_SENDER_PASSWORD = environ.get('MAIL_SENDER_PASSWORD')
    MAIL_SMTP_SERVER = environ.get('MAIL_SMTP_SERVER')
    MAIL_SMTP_PORT = int(environ.get('MAIL_SMTP_PORT'))

    CONTACT_ADDR = environ.get('CONTACT_ADDR')

    EXTERNAL_URL = environ.get('EXTERNAL_URL')

    DEBUG = environ.get('DEBUG', False)
    DEBUG_TB_INTERCEPT_REDIRECTS = environ.get('DEBUG_TB_INTERCEPT_REDIRECTS', False)

    LOG_LEVEL = environ.get('LOG_LEVEL', 'DEBUG').upper()
	
    
