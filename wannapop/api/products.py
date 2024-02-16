# En products.py

from . import api_bp
from .errors import not_found, bad_request
from .. import db_manager as db
from ..models import Product, Category, Order
from ..helper_json import json_request, json_response
from flask import current_app, jsonify, request
from .helper_auth import basic_auth, token_auth


@api_bp.route('/products', methods=['GET'])
def get_product_filtred():
    title = request.args.get('title')
    if title:
        Product.db_enable_debug()
        items_with_store = Product.query.filter_by(title=title).all()
    else:
        items_with_store = []
    data = Product.to_dict_collection(items_with_store)
    return jsonify(
            {
                'data': data, 
                'success': True
            }), 200

@api_bp.route('/products/<int:product_id>', methods=['GET'])
def get_product_details(product_id):
    Product.db_enable_debug()
    product = Product.get(product_id)

    if product:
        data = Product.to_dict(product)
        return jsonify(
            {
                'data': data, 
                'success': True
            }), 200  
    else:
        current_app.logger.debug(f"Product {product_id} not found")
        return not_found("Product not found")
    
@api_bp.route('/products/<int:product_id>/orders', methods=['GET'])
def listar_ofertas_por_producto(product_id):
    orders = Order.query.filter_by(product_id=product_id).all()
    if orders:
        data = [order.to_dict() for order in orders]
        return jsonify(
            {
                'data': data, 
                'success': True
            }), 200 
    else:
        current_app.logger.debug(f"Product {product_id} not found")
        return not_found("Product not found")

@api_bp.route('/products/<int:product_id>', methods=['PUT'])
@token_auth.login_required
def edit_product(product_id):
    product = Product.get(product_id)
    
    if product:
        data = json_request(['title', 'description', 'photo', 'price', 'category_id', 'seller_id'])
        
        if token_auth.current_user().id != product.seller_id:
            return jsonify(
                {
                    'error': 'Unauthorized', 
                    'message': 'You are not authorized to edit this product', 
                    'success': False
                }), 401

        try:
            product.update(**data)
            current_app.logger.debug("UPDATED product: {}".format(product.to_dict()))
            return jsonify(
                {
                    'data': product.to_dict(), 
                    'success': True
                }), 200
        except Exception as e:
            current_app.logger.debug(e)
            return jsonify(
                {   
                    'error': 'Bad Request',
                    'message': str(e),
                    'success': False
                }), 400
    else:
        current_app.logger.debug("Product {} not found".format(product_id))
        return not_found("Product not found")

    
