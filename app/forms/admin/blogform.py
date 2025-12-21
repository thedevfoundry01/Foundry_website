from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, BooleanField, SelectMultipleField, FileField, SubmitField, HiddenField, SelectField
from wtforms.validators import DataRequired, Length, Email
from app.models.article import Category, Article
from app.models.user import User

class ArticleForm(FlaskForm):
    title = StringField(
        'Title',
        validators=[DataRequired(), Length(min=5, max=255)],
        render_kw={"placeholder": "Enter the article title"}
    )
    slug = StringField(
        'Slug',
        validators=[DataRequired(), Length(min=5, max=255)],
        render_kw={"placeholder": "Enter the article slug (URL-friendly)"}
    )
    content = TextAreaField(
        'Content',
        validators=[DataRequired()],
        render_kw={"placeholder": "Write your content here", "rows": 10}
    )
    categories = SelectMultipleField(
        'Categories',
        coerce=int,
        render_kw={"placeholder": "Select categories for this article"}
    )
    tags = SelectMultipleField(
        'Tags',
        coerce=int,
        render_kw={"placeholder": "Select tags for this article"}
    )
    is_published = BooleanField('Publish this article?')
    is_featured = BooleanField('Featured this article?')
    featured_image = FileField('Upload Featured Image')
    submit = SubmitField('Save Artcile')


class CommentForm(FlaskForm):
    content = TextAreaField('Comment Content', validators=[DataRequired()])
    is_approved = BooleanField('Approved')
    name = StringField(
        'Name',
        validators=[DataRequired(), Length(min=2, max=100)],
        render_kw={"placeholder": "Enter the user's name"}
    )
    email = StringField(
        'Email',
        validators=[DataRequired(), Email()],
        render_kw={"placeholder": "Enter the user's email"}
    )
    article_id = SelectField('Article', coerce=int, validators=[DataRequired()])
    parent_id = HiddenField('Parent Comment ID', default=None)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.article_id.choices = [(article.id, article.title) for article in Article.query.all()]


class CategoryForm(FlaskForm):
    name = StringField('Category Name', validators=[DataRequired(), Length(max=50)])
    description = TextAreaField('Category Description', default= None)
    slug = StringField('Slug', validators=[DataRequired(), Length(max=50)])
    submit = SubmitField('Create')
    
class EditCategoryForm(FlaskForm):
    name = StringField('Category Name', validators=[DataRequired(), Length(max=50)])
    description = TextAreaField('Category Description', default= None)
    slug = StringField('Slug', validators=[DataRequired(), Length(max=50)])
    submit = SubmitField('Update')


class TagForm(FlaskForm):
    name = StringField(
        'Name', 
        validators=[DataRequired(), Length(max=50)],
        render_kw={"class": "form-control"}  # Add a CSS class
    )
    submit = SubmitField(
        'Submit',
        render_kw={"class": "btn btn-primary"}  # Add a CSS class to the submit button
    )

class EditTagForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    submit = SubmitField('Update')
    
    
    
