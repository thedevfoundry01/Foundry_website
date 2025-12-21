from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, BooleanField, FileField, SubmitField, SelectMultipleField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError
from app.models.user import User
from app.models.role import Role

class UserForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(max=100)])
    email = StringField('Email', validators=[DataRequired(), Email(), Length(max=100)])
    password = PasswordField('Password', validators=[
        DataRequired(),
        Length(min=6, max=100),
        EqualTo('confirm_password', message='Passwords must match.')
    ])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired()])
    roles = SelectMultipleField('Roles', coerce=int, validators=[DataRequired()])
    status = SelectField('Status', choices=[('active', 'Active'), ('inactive', 'Inactive')], default='active')
    profile_image = FileField('Profile Image (Optional)')

    def validate_email(self, email):
        """Check if email is already in use."""
        existing_user = User.query.filter_by(email=email.data).first()
        if existing_user:
            raise ValidationError('This email is already registered.')

    def validate_role_id(self, role_id):
        """Ensure the role exists in the database."""
        if not Role.query.get(role_id.data):
            raise ValidationError('Invalid role selected.')


class EditUserForm(FlaskForm):
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
    roles = SelectMultipleField('Roles', coerce=int, validators=[DataRequired()])
    status = SelectField(
        'Status',
        choices=[('active', 'Active'), ('inactive', 'Inactive')],
        validators=[DataRequired()],
        render_kw={"placeholder": "Select the user status"}
    )
    submit = SubmitField('Update User')
