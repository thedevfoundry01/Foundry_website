from app.extensions import db
from app.models.user import User
from app.models.role import Role
from app.models.permission import Permission

def seed_roles_and_permissions():
    # Define roles
    roles = {
        'admin': 'Admin role with full permissions',
        'editor': 'Editor role with limited permissions',
        'user': 'Regular user role'
    }

    # Create roles if they don’t exist
    role_objects = {}
    for role_name, role_desc in roles.items():
        role = Role.query.filter_by(name=role_name).first()
        if not role:
            role = Role(name=role_name, description=role_desc)
            db.session.add(role)
        role_objects[role_name] = role

    # Define entity-specific actions
    entity_permissions = {
        'users': ['create', 'read', 'update', 'delete'],
        'roles': ['create', 'read', 'update', 'delete'],
        'permissions': ['create', 'read', 'update', 'delete'],
        'articles': ['create', 'read', 'update', 'delete'],
        'categories': ['create', 'read', 'update', 'delete'],
        'comments': ['create','read','update', 'approve', 'delete'],
        'tags': ['create', 'read', 'update', 'delete'],
        'settings': ['create', 'read', 'update', 'delete'],
        'contacts': ['read','delete'],  # Only listing page
        'subscribers': ['read','delete'],  # Only listing page
        'profile': ['read'],  # Only listing page
        'dashboard': ['read'],  # Only listing page
    }

    # Create permissions
    for entity, actions in entity_permissions.items():
        for action in actions:
            permission_name = f"{action}_{entity}"
            permission = Permission.query.filter_by(name=permission_name).first()
            if not permission:
                permission = Permission(
                    name=permission_name,
                    description=f"Can {action} {entity}"
                )
                db.session.add(permission)

    db.session.commit()  # Commit all created permissions before assigning them

    # Assign all permissions to admin role
    admin_role = role_objects['admin']
    all_permissions = Permission.query.all()
    
    for permission in all_permissions:
        if permission not in admin_role.permissions:
            admin_role.permissions.append(permission)

    # Commit role-permission relationships
    db.session.commit()

