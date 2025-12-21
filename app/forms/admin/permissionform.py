from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, BooleanField, HiddenField
from wtforms.validators import DataRequired, Length

class PermissionForm(FlaskForm):
    name = StringField('Permission Name', validators=[DataRequired(), Length(max=80)])
    description = TextAreaField('Description', validators=[Length(max=255)])
    submit = SubmitField('Create Permission')

class EditPermissionForm(PermissionForm):
    submit = SubmitField('Update Permission')



    
class PermissionCheckboxForm(FlaskForm):
    permission_id = HiddenField()  # Stores the permission ID
    checked = BooleanField()  # Checkbox state
