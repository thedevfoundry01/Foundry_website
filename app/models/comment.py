from app.extensions import db


class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    article_id = db.Column(db.Integer, db.ForeignKey('articles.id'), nullable=False)
    name = db.Column(db.String(250), nullable=False)
    email = db.Column(db.String(250), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.now())
    is_approved = db.Column(db.Boolean, default=True)
    parent_id = db.Column(
        db.Integer,
        db.ForeignKey('comments.id', name='fk_comment_parent'),
        nullable=True
    )

    # Relationships
    article = db.relationship('Article', backref='comments')
    replies = db.relationship(
        'Comment',
        backref=db.backref('parent', remote_side=[id]),
        lazy='dynamic',
        cascade="all, delete-orphan"  # Ensure replies are removed when the parent comment is deleted
    )

    # Index for parent_id to optimize querying replies
    __table_args__ = (
        db.Index('ix_comments_parent_id', 'parent_id'),
    )

    # Soft delete field
    deleted_at = db.Column(db.DateTime, nullable=True)

    # Reply count for comments
    reply_count = db.Column(db.Integer, default=0)

    def update_reply_count(self):
        """Update the reply count for the comment."""
        self.reply_count = self.replies.count()
        db.session.commit()

    def can_reply(self, max_depth=3):
        """Check if a reply can be added within the allowed depth."""
        depth = 0
        current = self
        while current.parent:
            depth += 1
            current = current.parent
        return depth < max_depth
    