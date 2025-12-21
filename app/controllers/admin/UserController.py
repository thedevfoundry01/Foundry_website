# app/controllers/admin/UserController.py
from flask import render_template, request, redirect, session, flash, url_for
from app.models.user import User
from app.models.role import Role
from app.models.permission import Permission
from app.extensions import db
from app.forms.admin.userform import UserForm, EditUserForm

class UserController:

    def users():
        page = request.args.get('page', 1, type=int)
        per_page = 10
        users = User.query.order_by(User.id.desc()).paginate(page=page, per_page=per_page)
        return render_template('admin/users/index.html', users=users)
    
    
    @staticmethod
    def create_user():
        form = UserForm()
        form.roles.choices = [(role.id, role.name) for role in Role.query.all()]

        if form.validate_on_submit():
            user = User(
                name=form.name.data,
                email=form.email.data,
                password=form.password.data,
                status=form.status.data
            )
            # Add roles and permissions
            user.roles = Role.query.filter(Role.id.in_(form.roles.data)).all()

            db.session.add(user)
            db.session.commit()
            flash('User created successfully!', 'success')
            return redirect(url_for('admin.users'))

        return render_template('admin/users/create.html', form=form)

    @staticmethod
    def edit_user(id):
        user = User.query.get_or_404(id)
        form = EditUserForm(obj=user)
        form.roles.choices = [(role.id, role.name) for role in Role.query.all()]

        if form.validate_on_submit():
            user.name = form.name.data
            user.email = form.email.data
            user.status = form.status.data
            # Update roles and permissions
            user.roles = Role.query.filter(Role.id.in_(form.roles.data)).all()

            db.session.commit()
            flash('User updated successfully!', 'success')
            return redirect(url_for('admin.users'))

        form.roles.data = [role.id for role in user.roles]
        return render_template('admin/users/edit.html', form=form, user=user)

    @staticmethod
    def delete_user(id):
        """Delete an existing user"""
        user = User.query.get_or_404(id)
        
        try:
            db.session.delete(user)
            db.session.commit()
            flash('User deleted successfully!', 'success')
        except Exception as e:
            db.session.rollback()
            flash('User has articles. Delete the articles first, then delete the user.', 'danger')
        
        return redirect(url_for('admin.users'))

