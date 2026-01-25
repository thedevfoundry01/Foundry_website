from flask import Flask
from app.extensions import db
from app.config import Config
from app.models.site_setting import SiteSetting
from app.setup import *


def create_app():
    """Application Factory for initializing the Flask app."""
    app = Flask(__name__)
    app.config.from_object(Config)
    app.config['ENV'] = 'development'
    app.config['DEBUG'] = True

    # Initialize extensions
    initialize_extensions(app)

    # Configure security settings
    configure_security(app)

    # Setup logging
    configure_logging(app)
    
    setting(app)

    # Add global after-request handlers
    # app.after_request(add_security_headers)
    
    @app.route('/uploads/<filename>')
    def uploaded_file(filename):
        """Serve uploaded files."""
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename)
    
    

    # Register routes and blueprints
    register_blueprints(app)

    return app


