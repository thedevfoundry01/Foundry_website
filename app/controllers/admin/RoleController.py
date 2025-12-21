from flask import render_template, request, redirect, flash, url_for
from app.models.role import Role
from app.models.permission import Permission
from app.extensions import db
from app.forms.admin.roleform import RoleForm, EditRoleForm
from app.forms.admin.permissionform import PermissionCheckboxForm

class RoleController:
    
    @staticmethod
    def roles():
        page = request.args.get('page', 1, type=int)
        per_page = 10
        roles = Role.query.order_by(Role.id.desc()).paginate(page=page, per_page=per_page)
        return render_template('admin/roles/index.html', roles=roles)
    
    @staticmethod
    def create_role():
        permissions = Permission.query.all()
        form = RoleForm()

        if form.validate_on_submit():
            selected_permission_ids = request.form.getlist("permissions")

            new_role = Role(
                name=form.name.data,
                description=form.description.data
            )
            db.session.add(new_role)
            db.session.commit()

            # Assign selected permissions
            new_role.permissions = Permission.query.filter(Permission.id.in_(selected_permission_ids)).all()
            db.session.commit()

            flash('Role created successfully!', 'success')
            return redirect(url_for('admin.roles'))

        return render_template('admin/roles/create.html', form=form, available_permissions=permissions)

    @staticmethod
    def edit_role(id):
        role = Role.query.get_or_404(id)
        permissions = Permission.query.all()
        form = EditRoleForm(obj=role)

        if request.method == "GET":
            form.permissions.entries = [
                PermissionCheckboxForm(permission_id=str(p.id)) for p in permissions
            ]
            for entry, perm in zip(form.permissions.entries, permissions):
                entry.checked.data = perm in role.permissions

        if form.validate_on_submit():
            selected_permission_ids = request.form.getlist("permissions")
            role.name = form.name.data
            role.description = form.description.data
            role.permissions = Permission.query.filter(Permission.id.in_(selected_permission_ids)).all()

            db.session.commit()
            flash("Role updated successfully!", "success")
            return redirect(url_for("admin.roles"))

        return render_template(
            "admin/roles/edit.html",
            form=form,
            role=role,
            available_permissions=permissions
        )

    @staticmethod
    def delete_role(id):
        role = Role.query.get_or_404(id)
        db.session.delete(role)
        db.session.commit()
        flash('Role deleted successfully!', 'success')
        return redirect(url_for('admin.roles'))
