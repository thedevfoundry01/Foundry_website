from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, FieldList, FormField, SubmitField
from wtforms.validators import DataRequired, Length
from app.forms.admin.permissionform import PermissionCheckboxForm

class RoleForm(FlaskForm):
    name = StringField('Role Name', validators=[DataRequired(), Length(max=50)])
    description = TextAreaField('Description', validators=[Length(max=255)])
    permissions = FieldList(FormField(PermissionCheckboxForm))  # Checkboxes
    submit = SubmitField('Create')

class EditRoleForm(FlaskForm):
    name = StringField('Role Name', validators=[DataRequired(), Length(max=50)])
    description = TextAreaField('Description', validators=[Length(max=255)])
    permissions = FieldList(FormField(PermissionCheckboxForm))  # Checkboxes
    submit = SubmitField('Update')
