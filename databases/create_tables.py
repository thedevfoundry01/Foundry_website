import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app, db
from databases.seeder.site_setting_seeder import seed_site_settings
from databases.seeder.users_seeder import seed_users
from databases.seeder.roles_permissions_seeder import seed_roles_and_permissions

def create_tables():
    """Create all database tables."""
    print("Creating database tables...")
    db.create_all()
    print("Tables created successfully.")
    print("Seeding settings and users(admin)...")
    seed_site_settings()
    seed_roles_and_permissions()
    seed_users()
    print("completed")
    

if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        db.drop_all()
        create_tables()
