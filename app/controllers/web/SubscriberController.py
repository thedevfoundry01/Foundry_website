from flask import request, redirect, url_for, flash
from app.models.subscriber import Subscriber
from app.extensions import db
import re

class SubscriberController:
    @staticmethod
    def subscribe():
        if request.method == 'POST':
            email = request.form.get('email')

            # Validate email
            if not email or not re.match(r"[^@]+@[^@]+\.[^@]+", email):
                flash('Please provide a valid email address.', 'error')
                return redirect(url_for('web.home'))

            try:
                # Check if email already exists
                if Subscriber.query.filter_by(email=email).first():
                    flash('You are already subscribed!', 'info')
                else:
                    # Save to the database
                    subscriber = Subscriber(email=email)
                    db.session.add(subscriber)
                    db.session.commit()
                    flash('Thank you for subscribing!', 'success')
            except Exception as e:
                db.session.rollback()
                flash(f'An error occurred: {str(e)}', 'error')

        return redirect(url_for('web.home'))