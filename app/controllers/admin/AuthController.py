# app/controllers/admin/AuthController.py
from flask import render_template, request, redirect, flash, url_for
from flask_login import login_user, logout_user

from app.models.user import User
from app.models.article import Article
from app.models.comment import Comment
from app.models.subscriber import Subscriber
from datetime import datetime, timedelta

class AuthController:
    @staticmethod
    def login():
        """Handle admin login"""
        if request.method == 'POST':
            email = request.form['email']
            password = request.form['password']
            user = User.query.filter_by(email=email).first()

            if user and user.check_password(password):
                login_user(user)
                flash('Logged in successfully!', 'success')
                return redirect(url_for('admin.dashboard'))
            else:
                flash('Invalid credentials or not an admin', 'danger')
                return render_template('admin/login.html')

        return render_template('admin/login.html')
    
    @staticmethod
    def dashboard():
        total_users = User.query.count()
        total_articles = Article.query.count()
        total_comments = Comment.query.filter_by(is_approved=False).count()
        total_subscribers = Subscriber.query.count()

        # Generate user growth data (last 7 days)
        user_growth_dates = [(datetime.today() - timedelta(days=i)).strftime('%b %d') for i in range(7)][::-1]
        user_growth_numbers = [User.query.filter(User.created_at >= datetime.today() - timedelta(days=i)).count() for i in range(7)][::-1]

        # Post statistics (published, drafts, pending)
        published_articles = Article.query.filter_by(is_published=True).count()
        draft_articles = Article.query.filter_by(is_published=False).count()
        article_data = [published_articles, draft_articles]

        return render_template(
            'admin/dashboard.html',
            total_users=total_users,
            total_articles=total_articles,
            total_comments=total_comments,
            total_subscribers=total_subscribers,
            user_growth_dates=user_growth_dates,
            user_growth_numbers=user_growth_numbers,
            article_data=article_data
        )

    @staticmethod
    def logout():
        """Handle admin logout"""
        logout_user()  # Log out the user using Flask-Login
        flash('You have been logged out.', 'success')
        return redirect(url_for('admin.login'))
