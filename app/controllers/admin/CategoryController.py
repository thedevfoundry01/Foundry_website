from flask import render_template, request, redirect, session, flash, url_for
from app.models.article import Category
from app.extensions import db
from app.forms.admin.blogform import CategoryForm, EditCategoryForm


class CategoryController:
    
    @staticmethod
    def categories():
        page = request.args.get('page', 1, type=int)
        per_page = 10
        categories = Category.query.order_by(Category.id.desc()).paginate(page=page, per_page=per_page)
        return render_template('admin/categories/index.html',  categories=categories)
    
    @staticmethod
    def create_category():
        """Create a new category"""
        form = CategoryForm()
        if form.validate_on_submit():
            category = Category(name=form.name.data, slug=form.slug.data)
            db.session.add(category)
            db.session.commit()
            flash('Category created successfully!', 'success')
            return redirect('/admin/categories')
        
        return render_template('admin/categories/create.html', form=form)

    @staticmethod
    def edit_category(id):
        """Edit an existing category"""
        category = Category.query.get_or_404(id)
        form = EditCategoryForm(obj=category)
        if form.validate_on_submit():
            form.populate_obj(category)
            db.session.commit()
            flash('Category updated successfully!', 'success')
            return redirect(url_for('admin.categories'))
        
        return render_template('admin/categories/edit.html', form=form, category=category)

    @staticmethod
    def delete_category(id):
        """Delete an existing category"""
        category = Category.query.get_or_404(id)
        db.session.delete(category)
        db.session.commit()
        flash('Category deleted successfully!', 'success')
        return redirect(url_for('admin.categories'))
