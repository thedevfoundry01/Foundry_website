from flask import render_template, redirect, url_for, request, flash
from app.models.article import Article
from app.models.comment import Comment
from app.forms.admin.blogform import CommentForm
from app.extensions import db

class CommentController:
    @staticmethod
    def comments():
        """List all comments with pagination."""
        form = CommentForm()
        page = request.args.get('page', 1, type=int)
        per_page = 10
        comments_pagination = Comment.query.order_by(Comment.id.desc()).paginate(page=page, per_page=per_page)
        return render_template('admin/comments/index.html', comments_pagination=comments_pagination, form=form)

    @staticmethod
    def manage_comment(comment_id=None, parent_id=None):
        """Manage (edit or create) a comment, with support for replies."""
        comment = Comment.query.get(comment_id) if comment_id else None
        form = CommentForm(obj=comment)

        if parent_id:
            form.parent_id.data = parent_id  # Pre-fill hidden parent_id field for replies
        
        if form.validate_on_submit():
            post = Article.query.get(form.article_id.data)

            if not post:
                flash('Invalid article.', 'danger')
                return redirect(url_for('admin.manage_comment', comment_id=comment_id))

            if comment:
                # Update existing comment
                comment.content = form.content.data
                comment.name = form.name.data
                comment.email = form.email.data
                comment.is_approved = form.is_approved.data if form.is_approved is not None else False
                flash('Comment updated successfully!', 'success')
            else:
                # Create a new comment or reply
                new_comment = Comment(
                    content=form.content.data,
                    name=form.name.data,
                    email=form.email.data,
                    post_id=form.article_id.data,
                    parent_id=form.parent_id.data if form.parent_id.data else None,
                    is_approved=form.is_approved.data if form.is_approved is not None else False,
                )
                db.session.add(new_comment)
                flash('Comment added successfully!', 'success')

            db.session.commit()
            return redirect(url_for('admin.comments'))
        else:
            print(form.errors)
        
        return render_template('admin/comments/manage_comment.html', form=form, comment=comment)

    @staticmethod
    def approve_comment(comment_id):
        """Approve a comment."""
        comment = Comment.query.get_or_404(comment_id)
        
        if comment.is_approved:
            flash('Comment is already approved.', 'info')
        else:
            comment.is_approved = True
            db.session.commit()
            flash('Comment approved successfully!', 'success')
        
        return redirect(url_for('admin.comments'))
    
    
    @staticmethod
    def delete_comment(comment_id):
        """Delete a comment."""
        comment = Comment.query.get_or_404(comment_id)
        db.session.delete(comment)
        db.session.commit()
        flash('Comment deleted successfully!', 'success')
        return redirect(url_for('admin.comments'))