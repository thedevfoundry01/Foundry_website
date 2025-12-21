from flask import render_template, request, redirect, flash, url_for, current_app, jsonify
from slugify import slugify
from app.models.article import Article, Category, Tag
from app.extensions import db
from app.forms.admin.blogform import ArticleForm
import os
from werkzeug.utils import secure_filename
from flask_login import current_user

class ArticleController:

    @staticmethod
    def articles():
        """Display paginated list of articles."""
        page = request.args.get('page', 1, type=int)
        per_page = 10
        articles_pagination = Article.query.order_by(Article.id.desc()).paginate(page=page, per_page=per_page)
        return render_template('admin/articles/index.html', articles_pagination=articles_pagination)

    @staticmethod
    def manage_article(article_id=None):
        """Create or edit a article."""
        article = Article.query.get_or_404(article_id) if article_id else None
        
        if(article_id):
            author_id = article.author_id
        else:
            author_id = current_user.id
            
        form = ArticleForm(obj=article)

        # Populate dropdowns for categories and tags
        ArticleController._populate_form_choices(form)

        if form.validate_on_submit():
            article = article or Article(author_id=author_id)
            ArticleController._update_article_attributes(article, form)
            
            if form.featured_image.data:
                file_path = ArticleController._handle_featured_image_upload(form.featured_image.data)
                if file_path:
                    article.featured_image = file_path
            article.is_featured =  True if form.is_featured.data else False
            db.session.add(article)
            db.session.commit()
            flash('Article saved successfully!', 'success')
            return redirect(url_for('admin.articles'))

        # Pre-select existing categories and tags
        ArticleController._preselect_choices(article, form)
        return render_template('admin/articles/manage_article.html', form=form, article=article)

    @staticmethod
    def delete_article(article_id):
        """Delete an existing article."""
        article = Article.query.get_or_404(article_id)
        db.session.delete(article)
        db.session.commit()
        flash('Article deleted successfully!', 'success')
        return redirect(url_for('admin.articles'))

    # Helper methods
    @staticmethod
    def _populate_form_choices(form):
        """Populate form dropdowns for categories and tags."""
        form.categories.choices = [(category.id, category.name) for category in Category.query.all()]
        form.tags.choices = [(tag.id, tag.name) for tag in Tag.query.all()]

    @staticmethod
    def _update_article_attributes(article, form):
        """Update attributes of the article."""
        article.title = form.title.data
        article.slug = form.slug.data or slugify(form.title.data)
        article.content = form.content.data
        article.is_published = form.is_published.data
        article.categories = Category.query.filter(Category.id.in_(form.categories.data)).all()
        article.tags = Tag.query.filter(Tag.id.in_(form.tags.data)).all()

    @staticmethod
    def _preselect_choices(article, form):
        """Preselect existing categories and tags for a article."""
        if article:
            form.categories.data = [category.id for category in article.categories]
            form.tags.data = [tag.id for tag in article.tags]

    @staticmethod
    def _handle_featured_image_upload(featured_image_file):
        """Handle featured image upload and return the file path."""
        if not featured_image_file:
            return None

        # Ensure the file has a secure filename
        filename = secure_filename(featured_image_file.filename)
        if not ArticleController._is_allowed_file(filename):
            flash('Invalid file type. Only images are allowed.', 'danger')
            return None

        # Save the file
        upload_folder = current_app.config.get('UPLOAD_FOLDER')+'/articles'
        os.makedirs(upload_folder, exist_ok=True)  # Ensure the folder exists
        file_path = os.path.join(upload_folder, filename)
        featured_image_file.save(file_path)
        return filename

    @staticmethod
    def _is_allowed_file(filename):
        """Check if the file type is allowed."""
        allowed_extensions = {'png', 'jpg', 'jpeg', 'gif'}
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions

    @staticmethod
    def upload_image():
        """Handle image upload for Summernote."""
        if 'file' not in request.files:
            return jsonify({'error': 'No file part'}), 400
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No selected file'}), 400

        filename = secure_filename(file.filename)
        upload_folder = os.path.join(current_app.config['UPLOAD_FOLDER'], 'articles')
        os.makedirs(upload_folder, exist_ok=True)  # Ensure the folder exists
        file_path = os.path.join(upload_folder, filename)

        try:
            file.save(file_path)
            # You can now save the file URL or path to the database if needed
            file_url = url_for('static', filename=f'uploads/articles/{filename}')
            return jsonify({'url': file_url}), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500