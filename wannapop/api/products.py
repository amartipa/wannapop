# En products.py

from . import api_bp
from .errors import not_found, bad_request
from .. import db_manager as db
from ..models import Product, Category, Order
from ..helper_json import json_request, json_response
from flask import current_app, jsonify, request

@api_bp.route('/products', methods=['GET'])
def get_product_filtred():
    search = request.args.get('search')
    if search:
        Product.db_enable_debug()
        items_with_store = Product.filter_by_title(search)
    else:
        items_with_store = Product.db_query().order_by(Product.title.asc())
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
def edit_product(product_id):
    product = Product.get(product_id)
    if product:
        try:
            data = json_request(['title', 'description', 'photo', 'price', 'category_id', 'seller_id'])
        except Exception as e:
            current_app.logger.debug(e)
            return jsonify(
                {   
                    'error': 'Bad Request',
                    'message': str(e),
                    'success': False
                }), 400
        else:
            product.update(**data)
            current_app.logger.debug("UPDATED product: {}".format(product.to_dict()))
            return jsonify(
                {
                    'data': product.to_dict(), 
                    'success': True
                }), 200
    else:
        current_app.logger.debug("Product {} not found".format(product_id))
        return not_found("Product not found")

    
