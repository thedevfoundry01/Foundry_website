import sys
import os

# Add the project root to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app,db  # Import your app factory
from databases.seeder.articles_seeder import seed_articles
from databases.seeder.categories_seeder import seed_categories
from databases.seeder.tags_seeder import seed_tags
from databases.seeder.comments_seeder import seed_comments
from databases.seeder.users_seeder import seed_users
from databases.seeder.roles_permissions_seeder import seed_roles_and_permissions
from databases.seeder.site_setting_seeder import seed_site_settings
from databases.seeder.subscribes_seeder import seed_subscribers
from databases.create_tables import create_tables

def run_seeder():
    """Run all seeders."""
    
    print("Seeding database...")
    seed_roles_and_permissions()
    seed_users()
    seed_categories()
    seed_tags()
    seed_articles(30)
    seed_comments(20)
    seed_site_settings()
    seed_subscribers()
    print("Seeding complete.")

if __name__ == "__main__":
    app = create_app()
    # Use the app context
    with app.app_context():
        db.drop_all()
        create_tables()
        run_seeder()
