from flask import Blueprint, render_template, redirect, url_for, flash, current_app
from flask_login import current_user, login_required
from .models import Product, Category, User
from .forms import ProductForm, DeleteForm, RegisterForm, LoginForm
from .helper_role import require_view_permission, require_edit_permission, require_create_permission, require_delete_permission
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash
from . import db_manager as db
import uuid
import os
from config import Config
import secrets
from . import mail_manager as mail




# Blueprint
main_bp = Blueprint(
    "main_bp", __name__, template_folder="templates", static_folder="static"
)

@main_bp.route('/')
def init():
    if current_user.is_authenticated:
        return redirect(url_for('main_bp.product_list'))
    else:
        return redirect(url_for("auth_bp.login"))

@main_bp.route('/register', methods=['POST', 'GET'])
def wannapop_register():
    form = RegisterForm()

    if form.validate_on_submit():
        token = secrets.token_urlsafe(20)
        # Crea un nuevo objeto de usuario
        new_user = User(
            name=form.name.data, 
            email=form.email.data, 
            password=generate_password_hash(form.password.data),  # Aplica hash a la contraseña
            role='wanner',
            email_token=token,
            verified=0
        )

        # Agrega el nuevo usuario a la base de datos
        db.session.add(new_user)
        db.session.commit()
        msg = f"""
                URL: http://127.0.0.1:5000/verify/{new_user.name}/{token}
        """
        mail.send_contact_msg( msg, new_user.name, new_user.email)


        flash("Nou usuari creat", "success")
        return redirect(url_for('auth_bp.login'))
    else:
        # flash('Error al crear usuari', "error") se queda comentado por que al entrar en la pestaña de register salta el mensaje flash ants de rellenar el formulario
        return render_template('/users/register.html', form=form)
    

@main_bp.route('/verify/<name>/<email_token>')
def verify(name, email_token):
    user = User.query.filter_by(name=name, email_token=email_token).first()
        
    if user:
        if user.verified == 0:
            # Actualizar el estado de verificado y limpiar el token
            user.verified = 1
            user.email_token = None
            db.session.commit()
            flash("Tu cuenta ha sido verificada con éxito.", "success")
            return redirect(url_for('auth_bp.login'))
        else:
            flash("Esta cuenta ya ha sido verificada.", "info")
            return redirect(url_for('auth_bp.login'))
    else:
        # Manejo de error si no se encuentra el usuario o el token no coincide
        flash("Enlace de verificación inválido o caducado.", "error")
        return redirect(url_for('main_bp.index'))

    
@main_bp.route('/products/list')
@login_required
@require_view_permission.require(http_exception=403)
def product_list():
    # select amb join que retorna una llista dwe resultats
    products_with_category = db.session.query(Product, Category).join(Category).order_by(Product.id.asc()).all()
    
    return render_template('products/list.html', products_with_category = products_with_category)

@main_bp.route('/products/create', methods = ['POST', 'GET'])
@login_required
@require_create_permission.require(http_exception=403)
def product_create(): 

    # select que retorna una llista de resultats
    categories = db.session.query(Category).order_by(Category.id.asc()).all()

    # carrego el formulari amb l'objecte products
    form = ProductForm()
    form.category_id.choices = [(category.id, category.name) for category in categories]

    if form.validate_on_submit(): # si s'ha fet submit al formulari
        new_product = Product()
        new_product.seller_id = current_user.id 

        # dades del formulari a l'objecte product
        form.populate_obj(new_product)

        # si hi ha foto
        filename = __manage_photo_file(form.photo_file)
        if filename:
            new_product.photo = filename
        else:
            new_product.photo = "no_image.png"

        # insert!
        db.session.add(new_product)
        db.session.commit()

        # https://en.wikipedia.org/wiki/Post/Redirect/Get
        flash("Nou producte creat", "success")
        return redirect(url_for('main_bp.product_list'))
    else: # GET
        return render_template('products/create.html', form = form)

@main_bp.route('/products/read/<int:product_id>')
@login_required
@require_view_permission.require(http_exception=403)
def product_read(product_id):
    # select amb join i 1 resultat
    (product, category) = db.session.query(Product, Category).join(Category).filter(Product.id == product_id).one()
    
    return render_template('products/read.html', product = product, category = category)

@main_bp.route('/products/update/<int:product_id>',methods = ['POST', 'GET'])
@login_required
@require_edit_permission.require(http_exception=403)
def product_update(product_id):
    # select amb 1 resultat
    product = db.session.query(Product).filter(Product.id == product_id).one()

    # select que retorna una llista de resultats
    categories = db.session.query(Category).order_by(Category.id.asc()).all()

    # carrego el formulari amb l'objecte products
    form = ProductForm(obj = product)
    form.category_id.choices = [(category.id, category.name) for category in categories]

    if form.validate_on_submit(): # si s'ha fet submit al formulari
        # dades del formulari a l'objecte product
        form.populate_obj(product)

        # si hi ha foto
        filename = __manage_photo_file(form.photo_file)
        if filename:
            product.photo = filename

        # update!
        db.session.add(product)
        db.session.commit()

        # https://en.wikipedia.org/wiki/Post/Redirect/Get
        flash("Producte actualitzat", "success")
        return redirect(url_for('main_bp.product_read', product_id = product_id))
    else: # GET
        return render_template('products/update.html', product_id = product_id, form = form)

@main_bp.route('/products/delete/<int:product_id>',methods = ['GET', 'POST'])
@login_required
@require_delete_permission.require(http_exception=403)
def product_delete(product_id):
    # select amb 1 resultat
    product = db.session.query(Product).filter(Product.id == product_id).one()

    if current_user.id == product.seller_id:
        form = DeleteForm()
        if form.validate_on_submit(): # si s'ha fet submit al formulari
            # delete!
            db.session.delete(product)
            db.session.commit()

            flash("Producte esborrat", "success")
            return redirect(url_for('main_bp.product_list'))
        else: # GET
            return render_template('products/delete.html', form = form, product = product)
    else:
        flash('Error: No es por esborrar productes de terceres persones')
        return redirect(url_for('main_bp.product_read', product_id = product_id))




# __uploads_folder = os.path.join(Config.BASEDIR, Config.IMAGES_UPLOAD_PATH)
__uploads_folder = current_app.config.get("UPLOADS_FOLDER")
def __manage_photo_file(photo_file):
    # si hi ha fitxer
    if photo_file.data:
        filename = photo_file.data.filename.lower()

        # és una foto
        if filename.endswith(('.png', '.jpg', '.jpeg', '.jfif')):
            # M'asseguro que el nom del fitxer és únic per evitar col·lissions
            unique_filename = str(uuid.uuid4())+ "-" + secure_filename(filename)
            photo_file.data.save(__uploads_folder + unique_filename)
            return unique_filename

    return None

