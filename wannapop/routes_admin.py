from flask import Blueprint, render_template, redirect, flash, url_for
from flask_login import current_user, login_required
from .models import User, BlockedUser
from .helper_role import require_admin_role, require_admin_or_moderator_role
from . import db_manager as db
from datetime import datetime
from .forms import BlockUserForm

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
    return render_template('admin/users_list.html', users=users)

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
        db.session.add(blocked_user)
        db.session.commit()

        flash('El usuario ha sido bloqueado con éxito', 'success')
        return redirect(url_for('admin_bp.admin_users'))

    
    return render_template('block.html', form=form, user=user)
               
@admin_bp.route('/admin/users/<int:user_id>/unblock', methods=['POST'])
@login_required
@require_admin_role.require(http_exception=403)
def unblock_user(user_id):
    blocked_user = BlockedUser.query.filter_by(user_id=user_id).first()

    if blocked_user:
        db.session.delete(blocked_user)
        db.session.commit()
        flash('El usuario ha sido desbloqueado con éxito', 'success')
    else:
        flash('Este usuario no está bloqueado', 'error')

    return redirect(url_for('admin_bp.admin_users'))
 

        
    

    
        