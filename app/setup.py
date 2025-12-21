import json
from app.extensions import db, migrate, limiter, login_manager
from app.routes.admin import admin_bp
from app.routes.web import web_bp
from flask_wtf.csrf import CSRFProtect
import logging
from logging.handlers import RotatingFileHandler
from app.models.user import User
from app.models.site_setting import SiteSetting
from app.models.article import Category
import os


def initialize_extensions(app):
    """Initialize Flask extensions."""
    db.init_app(app)
    migrate.init_app(app, db)
    limiter.init_app(app)
    login_manager.init_app(app)
    # login_manager.login_view = 'auth.login'
    login_manager.login_message_category = 'info'

    # CSRF Protection
    CSRFProtect(app)


def configure_security(app):
    """Configure security-related settings for the application."""
    app.config['SESSION_COOKIE_HTTPONLY'] = True
    app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
    if app.config['ENV'] == 'production':
        app.config['SESSION_COOKIE_SECURE'] = True
        app.config['PREFERRED_URL_SCHEME'] = 'https'
    else:
        app.config['SESSION_COOKIE_SECURE'] = False
        app.config['PREFERRED_URL_SCHEME'] = 'http'


def configure_logging(app):
    """Configure application logging."""
    handler = RotatingFileHandler('app.log', maxBytes=10000, backupCount=3)
    handler.setLevel(logging.INFO)
    app.logger.addHandler(handler)


def add_security_headers(response):
    """Add security-related headers to responses."""
    response.headers['Content-Security-Policy'] = (
        "default-src 'self'; "
        "script-src 'self'; "
        "style-src 'self' 'unsafe-inline'; "
        "img-src 'self' data:; "
        "font-src 'self';"
    )
    return response


def register_blueprints(app):
    """Register application blueprints."""
    app.register_blueprint(admin_bp)
    app.register_blueprint(web_bp)



def setting(app):
    
    @login_manager.user_loader
    def load_user(user_id):
        user = User.query.get(int(user_id))
        return user

    @app.context_processor
    def inject_settings():
        settings = {setting.key: setting.value for setting in SiteSetting.query.all()}
        categories = Category.query.order_by(Category.name).all()
        return dict(settings=settings, categories=categories, config=app.config)

    def get_vite_asset(filename):
        manifest_path = os.path.join('app/static/dist/.vite/manifest.json')  # Corrected path

        if not os.path.exists(manifest_path):
            raise FileNotFoundError(f"Manifest file not found: {manifest_path}")

        with open(manifest_path) as f:
            manifest = json.load(f)

        key = f"src/{filename}"

        asset = manifest.get(key)
        
        if not asset:
            raise ValueError(f"Asset '{filename}' not found in manifest.json")

        js_file = asset["file"]
        css_file = asset["css"][0] if "css" in asset else None

        return js_file, css_file
    
    app.jinja_env.globals['get_vite_asset'] = get_vite_asset