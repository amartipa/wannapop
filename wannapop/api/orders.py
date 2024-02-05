from . import api_bp
from .errors import not_found, bad_request
from ..models import User, BlockedUser, Product, Order
from ..helper_json import json_request, json_response
from flask import current_app, request

#fer una oferta per un producte
@api_bp.route('/orders', methods=['POST'])
def create_order():
    try:
        data = json_request(['product_id','buyer_id','offer'])
    except Exception as e:
        current_app.logger.debug(e)
        return bad_request(str(e))
    else:
        order = Order.create(**data)
        current_app.logger.debug("CREATED Order: {}".format(order.to_dict()))
        return json_response(order.to_dict(), 201)
    
#update
@api_bp.route('orders/<int:id>', methods=['PUT'])
def update_order(id):
    order = Order.get(id)
    if order:
        try:
            data = json_request(['product_id','buyer_id','offer'])
        except Exception as e:
            current_app.logger.debug(e)
            return bad_request(str(e))
        else:
            order.update(**data)
            current_app.logger.debug("CREATED Order: {}".format(order.to_dict()))
            return json_response(order.to_dict())
    else:
        current_app.logger.debug("Order {} not found".format(id))
        return not_found("Order not found")
    
# Delete order
@api_bp.route('orders/<int:id>', methods=['DELETE'])
def delete_order(id):
    order = Order.get(id)
    if order:
        order.delete()
        current_app.logger.debug("Deleted Order: {}".format(id))
        return json_response(order.to_dict())
    else:
        current_app.logger.debug("Order {} notfound".format(id))
        return not_found("Item not found")

