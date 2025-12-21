from app.extensions import db

from datetime import datetime

class Subscriber(db.Model):
    __tablename__ = 'subscribes'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self,email):
        self.email = email
