from faker import Faker
from app.models.article import Category
from app.extensions import db
import slugify

faker = Faker()

def seed_categories():
    """Seed the database with predefined categories."""
    categories = ["Technology", "Science", "Health", "Education", "Travel"]
    for category_name in categories:
        # Generate a slug based on the category name
        slug = slugify.slugify(category_name)
        
        # Check if the category already exists to avoid duplicates
        existing_category = Category.query.filter_by(name=category_name).first()
        if not existing_category:
            category = Category(
                name=category_name,
                description=faker.text(max_nb_chars=200),
                slug=slug
                )
            db.session.add(category)
    
    db.session.commit()
    print("Seeded categories.")
