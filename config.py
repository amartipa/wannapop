from os import environ, path
from dotenv import load_dotenv

basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '.env'))

class Config:
    """Base config."""
    SECRET_KEY = environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + basedir + "/" + environ.get('SQLITE_FILE_RELATIVE_PATH')
    IMAGES_UPLOAD_PATH = environ.get('IMAGES_UPLOAD_PATH')  # Asegúrate de que esta variable está en tu archivo .env
    BASEDIR = basedir  # Añade basedir como un atributo de la clase Config
