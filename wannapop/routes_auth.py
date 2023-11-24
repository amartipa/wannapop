from flask import Blueprint, redirect, render_template, url_for, flash
from flask_login import current_user, login_user, login_required, logout_user
from . import login_manager
from .models import User
from .forms import LoginForm, RegisterForm
from .helper_role import notify_identity_changed
from werkzeug.security import check_password_hash,generate_password_hash
from . import db_manager as db
from werkzeug.security import check_password_hash

# Blueprint
auth_bp = Blueprint(
    "auth_bp", __name__, template_folder="templates", static_folder="static"
)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():

    if current_user.is_authenticated:
        return redirect(url_for("main_bp.init"))
        

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(name=form.username.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            flash('Login successful!')
            notify_identity_changed()
            return redirect(url_for('main_bp.product_list')) 
        else:
            flash('Invalid username or password')
            return redirect(url_for("auth_bp.login"))
    return render_template('users/login.html', form=form)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@login_manager.unauthorized_handler
def unauthorized():
    return redirect(url_for("auth_bp.login"))

@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("logged out succesfully")
    return redirect(url_for("auth_bp.login"))


