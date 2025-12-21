# app/routes/admin.py
from flask import Blueprint, render_template
from app.middlewares import admin_required, guest

from app.controllers.admin.AuthController import AuthController
from app.controllers.admin.UserController import UserController
from app.controllers.admin.RoleController import RoleController
from app.controllers.admin.PermissionController import PermissionController
from app.controllers.admin.ContactController import ContactController
from app.controllers.admin.TagController import TagController
from app.controllers.admin.ArticleController import ArticleController
from app.controllers.admin.CategoryController import CategoryController
from app.controllers.admin.CommentController import CommentController
from app.controllers.admin.ProfileController import ProfileController
from app.controllers.admin.SubscriberController import SubscriberController
from app.controllers.admin.SiteSettingsController import SiteSettingsController
admin_bp = Blueprint('admin', __name__)




@admin_bp.route('/admin/login', methods=['GET', 'POST'])
@guest
def login():
    return AuthController.login()

@admin_bp.route('/admin/logout')
@admin_required
def logout():
    return AuthController.logout()



@admin_bp.route('/admin/dashboard')
@admin_required
def dashboard():
    return AuthController.dashboard()


@admin_bp.route('/admin/contacts')
@admin_required
def contacts():
    return ContactController.contacts()

@admin_bp.route('/admin/contacts/<int:id>')
@admin_required
def view_contact(id):
    return ContactController.view_contact(id)

@admin_bp.route('/admin/contacts/delete/<int:id>', methods=['POST'])
@admin_required
def delete_contact(id):
    return ContactController.delete_contact(id)



# Users

@admin_bp.route('/admin/users')
@admin_required
def users():
    return UserController.users()

@admin_bp.route('/admin/create-user', methods=['GET', 'POST'])
@admin_required
def create_user():
    return UserController.create_user()

@admin_bp.route('/admin/users/edit/<int:id>', methods=['GET', 'POST'])
@admin_required
def edit_user(id):
    return UserController.edit_user(id)

@admin_bp.route('/admin/users/delete/<int:id>', methods=['POST'])
@admin_required
def delete_user(id):
    return UserController.delete_user(id)



# Roles

@admin_bp.route('/admin/roles', methods=['GET', 'POST'])
@admin_required
def roles():
    return RoleController.roles()

@admin_bp.route('/admin/create-role', methods=['GET', 'POST'])
@admin_required
def create_role():
    return RoleController.create_role()

@admin_bp.route('/admin/roles/edit/<int:id>', methods=['GET', 'POST'])
@admin_required
def edit_role(id):
    return RoleController.edit_role(id)

@admin_bp.route('/admin/roles/delete/<int:id>', methods=['POST'])
@admin_required
def delete_role(id):
    return RoleController.delete_role(id)



# Permissions
@admin_bp.route('/admin/permissions', methods=['GET', 'POST'])
@admin_required
def permissions():
    return PermissionController.permissions()

@admin_bp.route('/admin/create-permission', methods=['GET', 'POST'])
@admin_required
def create_permission():
    return PermissionController.create_permission()

@admin_bp.route('/admin/permissions/edit/<int:id>', methods=['GET', 'POST'])
@admin_required
def edit_permission(id):
    return PermissionController.edit_permission(id)

@admin_bp.route('/admin/permissions/delete/<int:id>', methods=['POST'])
@admin_required
def delete_permission(id):
    return PermissionController.delete_permission(id)



# Profile

@admin_bp.route('/admin/profile', methods=['get','POST'])
@admin_required
def profile():
    return ProfileController.profile()

@admin_bp.route('/admin/update-password', methods=['POST'])
@admin_required
def update_password():
    return ProfileController.updatePassword()



# Tags

@admin_bp.route('/admin/tags', methods=['GET', 'POST'])
@admin_required
def tags():
    return TagController.tags()

@admin_bp.route('/admin/create-tag', methods=['GET', 'POST'])
@admin_required
def create_tag():
    return TagController.create_tag()

@admin_bp.route('/admin/tags/edit/<int:id>', methods=['GET', 'POST'])
@admin_required
def edit_tag(id):
    return TagController.edit_tag(id)

@admin_bp.route('/admin/tags/delete/<int:id>', methods=['POST'])
@admin_required
def delete_tag(id):
    return TagController.delete_tag(id)

# Categories

@admin_bp.route('/admin/categories', methods=['GET', 'POST'])
@admin_required
def categories():
    return CategoryController.categories()

@admin_bp.route('/admin/create-category', methods=['GET', 'POST'])
@admin_required
def create_category():
    return CategoryController.create_category()

@admin_bp.route('/admin/categories/edit/<int:id>', methods=['GET', 'POST'])
@admin_required
def edit_category(id):
    return CategoryController.edit_category(id)

@admin_bp.route('/admin/categories/delete/<int:id>', methods=['POST'])
@admin_required
def delete_category(id):
    return CategoryController.delete_category(id)



# Articles
@admin_bp.route('/admin/articles', methods=['GET', 'POST'])
@admin_required
def articles():
    return ArticleController.articles()

@admin_bp.route('/admin/create-article', methods=['GET', 'POST'])
@admin_bp.route('/admin/articles/edit/<int:id>', methods=['GET', 'POST'])
@admin_required
def manage_article(id=None):
    return ArticleController.manage_article(id)

@admin_bp.route('/admin/articles/delete/<int:id>', methods=['POST'])
@admin_required
def delete_article(id):
    return ArticleController.delete_article(id)

@admin_bp.route('/admin/upload_image', methods=['POST'])
@admin_required
def upload_image():
    return ArticleController.upload_image()





# Comments
@admin_bp.route('/admin/comments', methods=['GET'])
@admin_required
def comments():
    return CommentController.comments()

@admin_bp.route('/admin/comments/manage/<int:comment_id>', methods=['GET', 'POST'])
@admin_bp.route('/admin/comments/manage', methods=['GET', 'POST'])
@admin_required
def manage_comment(comment_id=None):
    return CommentController.manage_comment(comment_id)

@admin_bp.route('/admin/comments/approve/<int:comment_id>', methods=['POST'])
@admin_required
def approve_comment(comment_id):
    return CommentController.approve_comment(comment_id)


@admin_bp.route('/admin/comments/delete/<int:comment_id>', methods=['POST'])
@admin_required
def delete_comment(comment_id):
    return CommentController.delete_comment(comment_id)


@admin_bp.route('/admin/comments/<int:comment_id>/reply', methods=['POST'])
@admin_required
def reply_to_comment(comment_id):
    return CommentController.reply_to_comment(comment_id)




@admin_bp.route('/site-settings', methods=['GET'])
@admin_required
def site_settings():
    return SiteSettingsController.index()

@admin_bp.route('/site-settings/create', methods=['GET'])
@admin_required
def create_site_setting():
    return SiteSettingsController.create()

@admin_bp.route('/site-settings/store', methods=['POST'])
@admin_required
def store_site_setting():
    return SiteSettingsController.store()

@admin_bp.route('/site-settings/<int:id>/edit', methods=['GET'])
@admin_required
def edit_site_setting(id):
    return SiteSettingsController.edit(id)

@admin_bp.route('/site-settings/<int:id>/update', methods=['POST'])
@admin_required
def update_site_setting(id):
    return SiteSettingsController.update(id)

@admin_bp.route('/site-settings/<int:id>/delete', methods=['POST'])
@admin_required
def delete_site_setting(id):
    return SiteSettingsController.delete(id)




# Subscribers
@admin_bp.route('/admin/subscribers', methods=['GET'])
@admin_required
def subscribers():
    return SubscriberController.subscribers()

@admin_bp.route('/admin/subscribers/delete/<int:id>', methods=['POST'])
@admin_required
def delete_subscriber(id):
    return SubscriberController.delete_subscriber(id)


@admin_bp.errorhandler(404)
def page_not_found(e):
    return render_template(
        'admin/errors/error.html',
        error_code=404,
        error_message="Page Not Found",
        error_description="The page you are looking for might have been removed, had its name changed, or is temporarily unavailable."
    ), 404

@admin_bp.errorhandler(500)
def internal_server_error(e):
    return render_template(
        'admin/errors/error.html',
        error_code=500,
        error_message="Internal Server Error",
        error_description="Something went wrong on our end. Please try again later or contact support if the issue persists."
    ), 500

@admin_bp.errorhandler(403)
def forbidden(e):
    return render_template(
        'admin/errors/error.html',
        error_code=403,
        error_message="Forbidden",
        error_description="You do not have permission to access this resource."
    ), 403

@admin_bp.errorhandler(401)
def unauthorized(e):
    return render_template(
        'admin/errors/error.html',
        error_code=401,
        error_message="Unauthorized",
        error_description="You need to log in to access this resource."
    ), 401
    
    