from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length

class ContactForm(FlaskForm):
    name = StringField('Contact Name', validators=[DataRequired(), Length(max=50)])
    message = TextAreaField('Description', validators=[Length(max=255)])
    submit = SubmitField('Create')
