from flask import render_template, request, redirect, session, flash, url_for
from app.models.contact import Contact
from app.extensions import db


class ContactController:
    
    @staticmethod
    def contacts():
        page = request.args.get('page', 1, type=int)
        per_page = 10
        contacts = Contact.query.order_by(Contact.id.desc()).paginate(page=page, per_page=per_page)
        return render_template('admin/contacts/index.html', contacts=contacts)
    
    @staticmethod
    def delete_contact(id):
        """Delete an existing contact"""
        contact = Contact.query.get_or_404(id)
        db.session.delete(contact)
        db.session.commit()
        flash('Contact deleted successfully!', 'success')
        return redirect(url_for('admin.contacts'))
    
    @staticmethod
    def view_contact(id):
        """View details of an existing contact"""
        contact = Contact.query.get_or_404(id)  # Fetch the contact by ID or return a 404 error if not found
        return render_template('admin/contacts/view.html', contact=contact)

