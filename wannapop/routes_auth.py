from flask import Blueprint, redirect, render_template, url_for, flash, request
from flask_login import current_user, login_user, login_required, logout_user
from . import login_manager
from .models import User
from .forms import LoginForm, RegisterForm
from .helper_role import notify_identity_changed
from werkzeug.security import check_password_hash,generate_password_hash
from . import db_manager as db
from werkzeug.security import check_password_hash
import secrets
from . import mail_manager as mail
from . import db_manager as db, logger

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
        logger.debug(f"Usuari {form.username.data} intenta autenticar-se")
        user = User.get_filtered_by(name=form.username.data)
        if user and check_password_hash(user.password, form.password.data):
            if user.verified == 1:
                login_user(user)
                flash('Login successful!')
                notify_identity_changed()
                logger.debug(f"Usuari {current_user.name} s'ha autenticat correctament")
                return redirect(url_for('main_bp.product_list'))
            else:
                flash('El teu compte no está verificat, ves al teu correu per verificar-lo', 'warning')
                logger.warning(f"Usuari {form.username.data} no ha verificat el seu correu")
                return redirect(url_for("auth_bp.login"))
        else:
            flash('Correu o contraseña no valids')
            logger.warning(f"Usuari {form.username.data} no s'ha autenticat correctament")
            return redirect(url_for("auth_bp.login"))

    return render_template('users/login.html', form=form)

@auth_bp.route('/resend', methods=['POST', 'GET'])
def resend_verification_email():
    if current_user.is_authenticated:
        return redirect(url_for('main_bp.product_list'))  # Redirigeix a la pàgina principal si l'usuari ja està autenticat

    if request.method == 'POST':
        email = request.form.get('email')
        user = User.get_filtered_by(email=email)

        if user and not user.verified:
            # Genera un nou token i envia el correu
            new_token = secrets.token_urlsafe(20)
            user.email_token = new_token
            user.save()
    
            msg = f"""
                URL: http://127.0.0.1:5000/verify/{user.name}/{new_token}
            """
            mail.send_contact_msg( msg, user.name, user.email)

            flash('Generat nou enllaç de verificació. Si us plau, comprova el teu correu.', 'info')
        else:
            flash('Compte no trobat o ja verificat.', 'warning')

        return redirect(url_for('auth_bp.login'))

    return render_template('users/resend_verification.html')

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

@auth_bp.route('/profile')
@login_required
def profile():
    return render_template('users/profile.html', user=current_user)
