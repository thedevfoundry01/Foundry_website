from app.extensions import db




# Association table for Article and Category
article_categories = db.Table(
    'article_categories',
    db.Column('article_id', db.Integer, db.ForeignKey('articles.id'), primary_key=True),
    db.Column('category_id', db.Integer, db.ForeignKey('categories.id'), primary_key=True)
)

# Association table for Article and Tag
article_tags = db.Table(
    'article_tags',
    db.Column('article_id', db.Integer, db.ForeignKey('articles.id'), primary_key=True),
    db.Column('tag_id', db.Integer, db.ForeignKey('tags.id'), primary_key=True)
)


class Category(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.Text, nullable=True)
    slug = db.Column(db.String(50), unique=True, nullable=False)
    
    # Relationships
    articles = db.relationship('Article', secondary=article_categories, back_populates='categories')


class Tag(db.Model):
    __tablename__ = 'tags'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    
    # Relationships
    articles = db.relationship('Article', secondary=article_tags, back_populates='tags')


class Article(db.Model):
    __tablename__ = 'articles'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    slug = db.Column(db.String(255), unique=True, nullable=False)
    content = db.Column(db.Text, nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.now())
    updated_at = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())
    is_published = db.Column(db.Boolean, default=False)
    is_featured = db.Column(db.Boolean, default=False)
    featured_image = db.Column(db.String(255), nullable=True)
    
    # Relationships
    categories = db.relationship('Category', secondary=article_categories, back_populates='articles')
    tags = db.relationship('Tag', secondary=article_tags, back_populates='articles')
    author = db.relationship('User', backref=db.backref('articles', lazy=True))


