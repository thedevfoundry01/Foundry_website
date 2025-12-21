from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, FieldList, FormField, SubmitField
from wtforms.validators import DataRequired, Length
from app.forms.admin.permissionform import PermissionCheckboxForm

class SettingForm(FlaskForm):
    key = StringField('key name', validators=[DataRequired(), Length(max=50)])
    value = TextAreaField('value')
    submit = SubmitField('Create')