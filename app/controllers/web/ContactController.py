from flask import request, redirect, url_for, flash, render_template
from app.models.contact import Contact
from app.extensions import db
import re

class ContactController:
    @staticmethod
    def contact():
        if request.method == 'POST':
            name = request.form.get('name')
            email = request.form.get('email')
            message = request.form.get('message')

            # Validate form data
            if not name or not email or not message:
                flash('All fields are required.', 'error')
            elif not re.match(r"[^@]+@[^@]+\.[^@]+", email):
                flash('Please provide a valid email address.', 'error')
            else:
                try:
                    # Save to database
                    new_contact = Contact(name=name, email=email, message=message)
                    db.session.add(new_contact)
                    db.session.commit()
                    flash('Your message has been sent successfully!', 'success')
                except Exception as e:
                    db.session.rollback()
                    flash(f'An error occurred: {str(e)}', 'error')

            return redirect(url_for('web.contact'))

        return render_template('pages/contact.html')