from flask import render_template, redirect, url_for, request, flash
from app.models.site_setting import SiteSetting
from app import db


class SiteSettingsController:
    @staticmethod
    def index():
        """List all site settings"""
        site_settings = SiteSetting.query.all()
        return render_template('admin/site_settings/index.html', site_settings=site_settings)

    @staticmethod
    def create():
        """Show form to create a new site setting"""
        return render_template('admin/site_settings/create.html')

    @staticmethod
    def store():
        """Store a new site setting"""
        key = request.form.get('key')
        value = request.form.get('value')

        if not key:
            flash("Key is required!", "danger")
            return redirect(url_for('admin.create_site_setting'))

        if SiteSetting.query.filter_by(key=key).first():
            flash("Key already exists!", "danger")
            return redirect(url_for('admin.create_site_setting'))

        setting = SiteSetting(key=key, value=value)
        db.session.add(setting)
        db.session.commit()

        flash("Site setting created successfully!", "success")
        return redirect(url_for('admin.site_settings'))

    @staticmethod
    def edit(id):
        """Show form to edit an existing site setting"""
        setting = SiteSetting.query.get_or_404(id)
        return render_template('admin/site_settings/edit.html', setting=setting)

    @staticmethod
    def update(id):
        """Update an existing site setting"""
        setting = SiteSetting.query.get_or_404(id)
        setting.key = request.form.get('key')
        setting.value = request.form.get('value')

        db.session.commit()
        flash("Site setting updated successfully!", "success")
        return redirect(url_for('admin.site_settings'))

    @staticmethod
    def delete(id):
        """Delete a site setting"""
        setting = SiteSetting.query.get_or_404(id)
        db.session.delete(setting)
        db.session.commit()
        flash("Site setting deleted successfully!", "success")
        return redirect(url_for('admin.site_settings'))
