from flask import render_template, redirect, url_for, request, flash, session
from app.models.subscriber import Subscriber
from app.extensions import db


class SubscriberController:
    @staticmethod
    def subscribers():
        """List all subscribers with pagination."""
        page = request.args.get('page', 1, type=int)
        per_page = 10
        subscribers_pagination = Subscriber.query.order_by(Subscriber.id.desc()).paginate(page=page, per_page=per_page)
        return render_template('admin/subscribers/index.html', subscribers_pagination=subscribers_pagination)
    
    @staticmethod
    def delete_subscriber(comment_id):
        """Delete a comment."""
        comment = Subscriber.query.get_or_404(comment_id)
        db.session.delete(comment)
        db.session.commit()
        flash('Subscriber deleted successfully!', 'success')
        return redirect(url_for('admin.subscribers'))
