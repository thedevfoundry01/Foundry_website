from app.models.article import Tag
from app.extensions import db

def seed_tags():
    """Seed the database with predefined tags."""
    tags = ["Python", "Flask", "Django", "React", "AI", "Machine Learning"]
    for tag_name in tags:
        existing_tag = Tag.query.filter_by(name=tag_name).first()
        if not existing_tag:
            tag = Tag(name=tag_name)
            db.session.add(tag)
            db.session.commit()
            
    print("Seeded tags.")
