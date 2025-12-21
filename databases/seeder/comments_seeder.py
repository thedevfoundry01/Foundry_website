from faker import Faker
from app.models.comment import Comment
from app.models.article import Article
from app.models.user import User
from app.extensions import db
import random

faker = Faker()

def seed_comments(count=20):
    """Seed the database with comments."""
    articles = Article.query.all()  # Get all articles
    users = User.query.all()  # Get all users

    if not articles:
        print("No articles found! Please seed articles first.")
        return
    if not users:
        print("No users found! Please seed users first.")
        return

    existing_comments = []

    for _ in range(count):
        # Create a random comment
        comment = Comment(
            content=faker.text(max_nb_chars=200),
            article_id=random.choice(articles).id,  # Assign random article
            name=faker.name(),
            email=faker.email(),
            is_approved=random.choice([True, False]),  # Randomize approval
        )

        # Randomly make this a reply to an existing comment
        if existing_comments and random.choice([True, False]):  # 50% chance to make it a reply
            comment.parent_id = random.choice(existing_comments).id

        db.session.add(comment)
        db.session.flush()  # Flush to get the comment ID for replies

        existing_comments.append(comment)  # Keep track of all comments

    db.session.commit()
    print(f"Seeded {count} comments.")
