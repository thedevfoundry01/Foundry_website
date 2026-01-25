from app.extensions import db
from flask_login import UserMixin
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask import current_app


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False) # Increased length for hashes
    profile_image = db.Column(db.String(255), default='default.png')
    status = db.Column(db.String(20), default='active')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    # Relationship with roles
    roles = db.relationship('Role', secondary='user_roles', back_populates='users')

    def __init__(self, name, email, password,status='active', profile_image=''):
        self.name = name
        self.email = email
        self.set_password(password)
        self.profile_image = profile_image
        self.status = status
        self.roles = []
        

    def has_role(self, role_name):
        return any(role.name == role_name for role in self.roles)
    
    def has_permission(self, permission_name):
        """Check if the user has a specific permission."""
        for role in self.roles:
            for permission in role.permissions:
                if permission.name == permission_name:
                    return True
        return False
    
    def has_any_permission(self, permission_names):
        for role in self.roles:
            for permission in role.permissions:
                if permission.name in permission_names:
                    return True
        return False
    
    
    def get_id(self):
        return str(self.id)
    
    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        if not self.password:
            return False
        try:
            return check_password_hash(self.password, password)
        except ValueError:
            # Handle invalid salt/hash errors gracefully
            return False

    def __repr__(self):
        return f"<User {self.name} ({self.email})>"


