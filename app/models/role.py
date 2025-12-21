from app.extensions import db

class Role(db.Model):
    __tablename__ = 'roles'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.Text, nullable=True)
    

    # Relationship with User
    users = db.relationship('User', secondary='user_roles', back_populates='roles')
    # Relationship with Permission
    permissions = db.relationship('Permission', secondary='role_permissions', back_populates='roles')


    def __repr__(self):
        return f"<Role {self.name}>"
