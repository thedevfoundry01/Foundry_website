from flask import render_template, request, redirect, flash, url_for
from app.models.permission import Permission
from app.extensions import db
from app.forms.admin.permissionform import PermissionForm, EditPermissionForm

class PermissionController:
    @staticmethod
    def permissions():
        page = request.args.get('page', 1, type=int)
        per_page = 10
        permissions = Permission.query.order_by(Permission.id.desc()).paginate(page=page, per_page=per_page)
        return render_template('admin/permissions/index.html', permissions=permissions)
    
    @staticmethod
    def create_permission():
        form = PermissionForm()
        if form.validate_on_submit():
            new_permission = Permission(name=form.name.data, description=form.description.data)
            db.session.add(new_permission)
            db.session.commit()
            flash('Permission created successfully!', 'success')
            return redirect(url_for('admin.permissions'))
        
        return render_template('admin/permissions/create.html', form=form)

    @staticmethod
    def edit_permission(id):
        permission = Permission.query.get_or_404(id)
        form = EditPermissionForm(obj=permission)
        if form.validate_on_submit():
            form.populate_obj(permission)
            db.session.commit()
            flash('Permission updated successfully!', 'success')
            return redirect(url_for('admin.permissions'))
        
        return render_template('admin/permissions/edit.html', form=form, permission=permission)

    @staticmethod
    def delete_permission(id):
        permission = Permission.query.get_or_404(id)
        db.session.delete(permission)
        db.session.commit()
        flash('Permission deleted successfully!', 'success')
        return redirect(url_for('admin.permissions'))
