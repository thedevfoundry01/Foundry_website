from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_limiter import Limiter
from flask_login import LoginManager
from flask import request
from flask_principal import Principal

# Initialize extensions
db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
limiter = Limiter(key_func=lambda: request.headers.get('X-Forwarded-For', request.remote_addr).split(',')[0].strip())
principal = Principal()


def init_extensions(app):
    """Initialize all extensions with the Flask app."""
    # Initialize SQLAlchemy and Flask-Migrate
    db.init_app(app)
    migrate.init_app(app, db)

    # Initialize Flask-Limiter
    limiter.init_app(app)
    
    principal.init_app(app)

    # Initialize Flask-Login
    login_manager.init_app(app)
    login_manager.login_view = 'admin.login'
