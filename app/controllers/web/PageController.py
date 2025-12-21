from flask import render_template
from app.models.article import Article

class PageController:
    @staticmethod
    def home():
        featured_articles = Article.query.filter_by(is_featured=True, is_published=True).order_by(Article.created_at.desc()).all()
        latest_articles = Article.query.filter_by(is_published=True).order_by(Article.created_at.desc()).limit(5).all()
        return render_template('pages/index.html', featured_articles=featured_articles, latest_articles=latest_articles)

    @staticmethod
    def about():
        return render_template('pages/about.html')

    @staticmethod
    def contact():
        return render_template('pages/contact.html')