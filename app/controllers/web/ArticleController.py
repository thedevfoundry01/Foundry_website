from flask import request, render_template, redirect, url_for, flash
from app.models.article import Article, Category, article_categories
from app.models.comment import Comment
from app.extensions import db

class ArticleController:
    @staticmethod
    def articles():
        page = request.args.get('page', 1, type=int)
        per_page = 8
        articles = Article.query.order_by(Article.created_at.desc()).paginate(page=page, per_page=per_page)
        return render_template('pages/articles/index.html', articles=articles)

    @staticmethod
    def article_detail(slug):
        article = Article.query.filter_by(slug=slug).first_or_404()
        comments = Comment.query.filter_by(article_id=article.id, parent_id=None).order_by(Comment.created_at.desc()).all()
        return render_template('pages/articles/detail.html', article=article, comments=comments)

    @staticmethod
    def category_articles(slug):
        category = Category.query.filter_by(slug=slug).first_or_404()
        page = request.args.get('page', 1, type=int)
        per_page = 10
        articles = (
            Article.query.join(article_categories, Article.id == article_categories.c.article_id)
            .filter(article_categories.c.category_id == category.id)
            .order_by(Article.created_at.desc())
            .paginate(page=page, per_page=per_page)
        )
        return render_template('pages/articles/category.html', category=category, articles=articles)

    @staticmethod
    def add_comment(slug):
        if request.method == 'POST':
            content = request.form.get('content')
            name = request.form.get('name')
            email = request.form.get('email')
            article = Article.query.filter_by(slug=slug).first_or_404()

            if not content or not name or not email:
                flash('All fields are required.', 'error')
            else:
                try:
                    comment = Comment(article_id=article.id, name=name, email=email, content=content)
                    db.session.add(comment)
                    db.session.commit()
                    flash('Your comment has been posted!', 'success')
                except Exception as e:
                    db.session.rollback()
                    flash(f'An error occurred: {str(e)}', 'error')

        return redirect(url_for('web.article_detail', slug=slug))

    @staticmethod
    def add_reply(comment_id):
        if request.method == 'POST':
            content = request.form.get('reply_content')
            name = request.form.get('name')
            email = request.form.get('email')
            parent_comment = Comment.query.filter_by(id=comment_id).first_or_404()

            if not content:
                flash('Reply content is required.', 'error')
            else:
                try:
                    reply = Comment(article_id=parent_comment.article_id, name=name, email=email, content=content, parent_id=parent_comment.id)
                    db.session.add(reply)
                    db.session.commit()
                    flash('Your reply has been posted!', 'success')
                except Exception as e:
                    db.session.rollback()
                    flash(f'An error occurred: {str(e)}', 'error')

        article = Article.query.get(parent_comment.article_id)
        return redirect(url_for('web.article_detail', slug=article.slug))

    @staticmethod
    def article_preview(slug):
        article = Article.query.filter_by(slug=slug).first_or_404()
        comments = Comment.query.filter_by(article_id=article.id, parent_id=None).order_by(Comment.created_at.desc()).all()
        return render_template('pages/articles/detail.html', article=article, comments=comments)