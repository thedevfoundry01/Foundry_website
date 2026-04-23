import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    # Environment
    ENV = os.getenv('FLASK_ENV')

    # Database Config
    SECRET_KEY = os.getenv('SECRET_KEY', 'your_secret_key')
    SECURITY_PASSWORD_SALT = os.getenv('SECURITY_PASSWORD_SALT', 'your-security-password-salt')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI', 'sqlite:///database.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Language Config
    BABEL_DEFAULT_LOCALE = os.getenv('BABEL_DEFAULT_LOCALE', 'en')
    BABEL_TRANSLATION_DIRECTORIES = os.getenv('BABEL_TRANSLATION_DIRECTORIES', 'translations')
    
    # Assets Config
    UPLOAD_FOLDER = os.getenv('UPLOAD_FOLDER', os.path.join(os.path.dirname(__file__), 'static/uploads'))  # Absolute path to uploads folder
    MAX_CONTENT_LENGTH = int(os.getenv('MAX_CONTENT_LENGTH', 2 * 1024 * 1024))  # 2 MB max file size by default
    