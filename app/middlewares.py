from functools import wraps
from app.models.user import User
from flask_login import current_user
from flask import url_for

from flask import session, redirect, flash, abort, url_for
from flask_principal import Permission, RoleNeed

def guest(func):
    """Decorator to ensure the user is not authenticated (guest)."""
    @wraps(func)
    def decorated(*args, **kwargs):
        if current_user.is_authenticated:
            flash('You are already logged in.', 'info')
            return redirect(url_for('admin.dashboard'))
        return func(*args, **kwargs)
    return decorated


def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            flash('Please log in to access this page.', 'warning')
            return redirect(url_for('admin.login'))

        return f(*args, **kwargs)
    
    return decorated_function
