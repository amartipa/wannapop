from flask import Blueprint, render_template, redirect, flash, url_for
from flask_login import current_user, login_required
from .models import User, BlockedUser, Product, BannedProduct
from .helper_role import require_admin_role, require_admin_or_moderator_role, require_moderator_role
from . import db_manager as db
from datetime import datetime
from .forms import BlockUserForm, BanProductForm

# Blueprint
admin_bp = Blueprint(
    "admin_bp", __name__, template_folder="templates/admin", static_folder="static"
)

@admin_bp.route('/admin')
@login_required
@require_admin_or_moderator_role.require(http_exception=403)

def admin_index():
    return render_template('admin/index.html')

@admin_bp.route('/admin/users')
@login_required
@require_admin_role.require(http_exception=403)
def admin_users():
    users = db.session.query(User).all()
    blocked_users = BlockedUser.query.with_entities(BlockedUser.user_id).all()
    blocked_user_ids = {bu.user_id for bu in blocked_users}
    return render_template('admin/users_list.html', users=users, blocked_user_ids=blocked_user_ids)

@admin_bp.route('/admin/users/<int:user_id>/block', methods=['POST', 'GET'])
@login_required
@require_admin_role.require(http_exception=403)
def block_users(user_id):
    user = db.session.query(User).filter(User.id == user_id).one()
    form = BlockUserForm()

    already_blocked = BlockedUser.query.filter_by(user_id=user_id).first()

    if already_blocked:
        flash('Este usuario ya está bloqueado.', 'error')
        return redirect(url_for('admin_bp.admin_users'))

    if form.validate_on_submit():
        # Crear un nuevo usuario bloqueado
        blocked_user = BlockedUser(user_id=user.id, message=form.message.data, created=datetime.now())
        blocked_user.save()

        flash('El usuario ha sido bloqueado con éxito', 'success')
        return redirect(url_for('admin_bp.admin_users'))

    
    return render_template('block.html', form=form, user=user)
               
@admin_bp.route('/admin/users/<int:user_id>/unblock', methods=['POST'])
@login_required
@require_admin_role.require(http_exception=403)
def unblock_user(user_id):
    blocked_user = BlockedUser.query.filter_by(user_id=user_id).first()

    if blocked_user:
        blocked_user.delete()
        flash('El usuario ha sido desbloqueado con éxito', 'success')
    else:
        flash('Este usuario no está bloqueado', 'error')

    return redirect(url_for('admin_bp.admin_users'))
 
@admin_bp.route('/admin/products')
@login_required
@require_moderator_role.require(http_exception=403)
def admin_products():
    products = db.session.query(Product).all()
    banned_product = BannedProduct.query.with_entities(BannedProduct.product_id).all()
    banned_products_id = {bp.product_id for bp in banned_product}
    return render_template('admin/products_list.html', products=products,banned_products_id = banned_products_id)

@admin_bp.route('/admin/products/<int:product_id>/ban', methods=['POST', 'GET'])
@login_required
@require_moderator_role.require(http_exception=403)
def ban_products(product_id):
    product = db.session.query(Product).filter(Product.id == product_id).one()
    form = BanProductForm()

    already_ban = BannedProduct.query.filter_by(product_id=product_id).first()

    if already_ban:
        flash('Este producto ya está bloqueado.', 'error')
        return redirect(url_for('admin_bp.admin_products'))

    if form.validate_on_submit():
        ban_product = BannedProduct(product_id=product_id, reason=form.reason.data, created=datetime.now())
        ban_product.save()

        flash('El producto ha sido bloqueado con éxito', 'success')
        return redirect(url_for('admin_bp.admin_products'))

    
    return render_template('ban.html', form=form, product=product)
               
@admin_bp.route('/admin/products/<int:product_id>/unban', methods=['POST'])
@login_required
@require_moderator_role.require(http_exception=403)
def unban_product(product_id):
    ban_product = BannedProduct.query.filter_by(product_id=product_id).first()

    if ban_product:
        ban_product.delete()
        flash('El producto ha sido desbloqueado con éxito', 'success')
    else:
        flash('Este usuario no está bloqueado', 'error')

    return redirect(url_for('admin_bp.admin_products'))

        
    

    
        