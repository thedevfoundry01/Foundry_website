from app.extensions import db

class Permission(db.Model):
    __tablename__ = 'permissions'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.Text, nullable=True)
    
    # Relationship with Role
    roles = db.relationship('Role', secondary='role_permissions', back_populates='permissions')
    
    def __repr__(self):
        return f"<Permission {self.name}>"


# UserRoles table to link users and roles
class UserRoles(db.Model):
    __tablename__ = 'user_roles'
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'), primary_key=True)

# RolePermissions table to link roles and permissions
class RolePermissions(db.Model):
    __tablename__ = 'role_permissions'
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'), primary_key=True)
    permission_id = db.Column(db.Integer, db.ForeignKey('permissions.id'), primary_key=True)
    