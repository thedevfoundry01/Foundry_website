from flask import Blueprint
from flask import Blueprint, request, render_template, redirect, session, flash, url_for
from app.controllers.web.PageController import PageController
from app.controllers.web.ContactController import ContactController
from app.controllers.web.ArticleController import ArticleController
from app.controllers.web.SubscriberController import SubscriberController

web_bp = Blueprint('web', __name__)


@web_bp.route('/')
def home():
    return PageController.home()

@web_bp.route('/about')
def about():
    return PageController.about()

@web_bp.route('/contact', methods=['GET', 'POST'])
def contact():
    return ContactController.contact()

@web_bp.route('/categories/<slug>')
def category_articles(slug):
    return ArticleController.category_articles(slug)

@web_bp.route('/articles')
def articles():
    return ArticleController.articles()

@web_bp.route('/articles/<slug>')
def article_detail(slug):
    return ArticleController.article_detail(slug)

@web_bp.route('/articles/<slug>/comment',  methods=['POST'])
def add_comment(slug):
    return ArticleController.add_comment(slug)


@web_bp.route('/comments/<int:comment_id>/reply', methods=['POST'])
def add_reply(comment_id):
    return ArticleController.add_reply(comment_id)


@web_bp.route('/articles/preview/<slug>')
def article_preview(slug):
    return ArticleController.article_preview(slug)


@web_bp.route('/subscribe', methods=['POST'])
def subscribe():
    return SubscriberController.subscribe()




@web_bp.errorhandler(404)
def page_not_found(e):
    return render_template(
        'pages/errors/404.html',
        error_code=404,
    ), 404

@web_bp.errorhandler(500)
def internal_server_error(e):
    return render_template(
        'pages/errors/500.html',
        error_code=500,
    ), 500