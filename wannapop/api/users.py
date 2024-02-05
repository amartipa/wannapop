from . import api_bp
from .errors import not_found, bad_request
from ..models import User, BlockedUser, Product
from ..helper_json import json_request, json_response
from flask import current_app, request

#List
@api_bp.route('/users', methods=['GET'])
def get_users():

    search = request.args.get('name')
    if search:
        #mostrar sql al terminal
        User.db_enable_debug()
        #filtrar usando el palametro
        my_filter = User.name.like('%'+search+'%')
        users = User.query.filter(my_filter).all()
    else:
        #sense filtrar
        users = User.get_all()
    data = User.to_dict_collection(users)
    return json_response(data)

@api_bp.route('/users/<int:id>', methods=['GET'])
def get_user(id):
    user = User.get(id)
    if user:
        data = user.to_dict()
        return json_response(data)
    else:
        current_app.logger.debug("User {} not found".format(id))
        return not_found("User not found")
    
@api_bp.route('/users/<int:id>/products')
def get_user_products(id):
    products = Product.get_all_filtered_by(seller_id = id)
    data = Product.to_dict_collection(products)
    return json_response(data)
   

