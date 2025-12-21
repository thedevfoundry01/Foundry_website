from flask import render_template, request, redirect, session, flash, url_for
from app.models.article import Tag
from app.extensions import db
from app.forms.admin.blogform import TagForm, EditTagForm


class TagController:
    
    @staticmethod
    def tags():
        page = request.args.get('page', 1, type=int)
        per_page = 10
        tags = Tag.query.order_by(Tag.id.desc()).paginate(page=page, per_page=per_page)
        return render_template('admin/tags/index.html', tags=tags)
    
    @staticmethod
    def create_tag():
        """Create a new tag"""
        form = TagForm()
        if form.validate_on_submit():
            tag = Tag(name=form.name.data)
            db.session.add(tag)
            db.session.commit()
            flash('Tag created successfully!', 'success')
            return redirect('/admin/tags')
        
        return render_template('admin/tags/create.html', form=form)

    @staticmethod
    def edit_tag(id):
        """Edit an existing tag"""
        tag = Tag.query.get_or_404(id)
        form = EditTagForm(obj=tag)
        if form.validate_on_submit():
            form.populate_obj(tag)
            db.session.commit()
            flash('Tag updated successfully!', 'success')
            return redirect(url_for('admin.tags'))
        
        return render_template('admin/tags/edit.html', form=form, tag=tag)

    @staticmethod
    def delete_tag(id):
        """Delete an existing tag"""
        tag = Tag.query.get_or_404(id)
        db.session.delete(tag)
        db.session.commit()
        flash('Tag deleted successfully!', 'success')
        return redirect(url_for('admin.tags'))
