from faker import Faker
from app.models.subscriber import Subscriber
from app.extensions import db
import random

faker = Faker()

def seed_subscribers(count=5):
    """Seed the database with subscribers."""
    existing_subscribers = []

    for _ in range(count):
        # Create a random comment
        subscriber = Subscriber(email=faker.email())
        db.session.add(subscriber)
        db.session.flush()
        existing_subscribers.append(subscriber)

    db.session.commit()
    print(f"Seeded {count} subscribers.")
