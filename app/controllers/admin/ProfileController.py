from flask import render_template, session, request, flash, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from flask import current_app
from app.extensions import db
from app.models.user import User
import os
from flask_login import current_user

class ProfileController:
    @staticmethod
    def profile():
        user = current_user
        
        if not user:
            # Handle the case where the user is not found
            return "User not found", 404
        
        if request.method == 'POST':
            name = request.form.get('name')
            email = request.form.get('email')
            profile_image = request.files.get('profile_image')
            
            if not name or not email:
                flash('Name and Email are required', 'danger')
                return redirect(url_for('admin.profile'))
            
            # Check if the new email already exists and is not the current user's email
            existing_user = User.query.filter_by(email=email).first()
            if existing_user and existing_user.id != user.id:
                flash('Email already exists. Please use a different email.', 'danger')
                return redirect(url_for('admin.profile'))
            
             # Handle profile image upload
            if profile_image and ProfileController.allowed_file(profile_image.filename):
                filename = secure_filename(profile_image.filename)
                image_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
                profile_image.save(image_path)
                user.profile_image = filename
            # Update the user's profile details
            user.name = name
            user.email = email
            db.session.commit()
            
            flash('Profile details updated successfully', 'success')
            return redirect(url_for('admin.profile'))
        
        return render_template('admin/profile.html', user=user)
    @staticmethod
    def updatePassword():
        """Handle password updates."""
        # Get the currently logged-in user
        auth_email = session.get('email')

        user = User.query.filter_by(email=auth_email).first()
        if not user:
            flash("User not found.", "danger")
            return redirect(url_for('auth.login'))

        # Get form data
        current_password = request.form.get('current_password')
        new_password = request.form.get('new_password')
        confirm_password = request.form.get('confirm_password')

        # Validate current password
        if not user.check_password(current_password):
            flash("Current password is incorrect.", "danger")
            return redirect(url_for('admin.profile'))

        # Check new password and confirmation
        if not new_password or new_password != confirm_password:
            flash("New password and confirm password must match.", "danger")
            return redirect(url_for('admin.profile'))

        # Update the password
        user.set_password(new_password)
        db.session.commit()

        flash("Password updated successfully!", "success")
        return redirect(url_for('admin.profile'))
    
    
    @staticmethod
    def allowed_file(filename):
        ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS