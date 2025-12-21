from app.extensions import db
from app.models.user import User
from app.models.role import Role
from app.models.permission import Permission
from app import create_app

app = create_app()

def seed_users():
    # Create admin user
    admin_role = Role.query.filter_by(name='admin').first()
    admin_user = User.query.filter_by(email='admin@example.com').first()
    if not admin_user:
        admin_user = User(
            name='Admin',
            email='admin@example.com',
            password='admin123',
            profile_image='avatar.png'
        )
        admin_user.roles.append(admin_role)  # Assign the admin role
        db.session.add(admin_user)
        print("Created admin user: admin@example.com / admin123")
    else:
        print("Admin user already exists.")

    # Create normal user
    user_role = Role.query.filter_by(name='user').first()
    normal_user = User.query.filter_by(email='user@example.com').first()
    if not normal_user:
        normal_user = User(
            name='Normal User',
            email='user@example.com',
            password='user123',
            profile_image='user.png'
        )
        normal_user.roles.append(user_role)  # Assign the user role
        db.session.add(normal_user)
    else:
        print("Normal user already exists.")

    db.session.commit()

