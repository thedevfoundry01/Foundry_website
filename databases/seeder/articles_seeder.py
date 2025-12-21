from faker import Faker
from app.models.article import Article,Category, Tag
from app.models.user import User
from app.extensions import db
from slugify import slugify
import random

faker = Faker()

def seed_articles(count=10):
    """Seed the database with articles."""
    users = User.query.all()
    categories = Category.query.all()
    tags = Tag.query.all()

    if not users:
        print("No users found! Please seed users first.")
        return

    if not categories:
        print("No categories found! Please seed categories first.")
        return
    

    for index in range(count):
        image_url = "thumbnail.jpg"
        title = faker.sentence()
        slug = slugify(title)
        article = Article(
            title=title,
            slug=slug,
            content=faker.text(max_nb_chars=500),
            author_id=random.choice(users).id,
            is_published=random.choice([True, False]),
            is_featured=random.choice([True, False]),
            featured_image= image_url
        )
        
        # Assign random categories and tags
        article.categories = random.sample(categories, k=random.randint(1, len(categories)))
        article.tags = random.sample(tags, k=random.randint(1, len(tags)))

        db.session.add(article)

    db.session.commit()
    print(f"Seeded {count} articles.")
