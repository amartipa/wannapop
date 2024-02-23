from . import api_bp
from .errors import not_found, bad_request, forbidden_access
from ..models import User, BlockedUser, Product, Order, ConfirmedOrder
from ..helper_json import json_request, json_response
from flask import current_app, request, jsonify
from .helper_auth import basic_auth, token_auth


#fer una oferta per un producte
# @api_bp.route('/orders', methods=['POST'])
# def create_order():
#     try:
#         data = json_request(['product_id','buyer_id','offer'])
#     except Exception as e:
#         current_app.logger.debug(e)
#         return bad_request(str(e))
#     else:
#         order = Order.create(**data)
#         current_app.logger.debug("CREATED Order: {}".format(order.to_dict()))
#         return json_response(order.to_dict(), 201)
@api_bp.route('/orders', methods=['POST'])
@token_auth.login_required
def create_order():

    data = json_request(['product_id', 'offer'])
    order = Order.get_all_filtered_by(product_id=data['product_id'],buyer_id=basic_auth.current_user().id)
    
    if not order:
        try:

            data['buyer_id'] = basic_auth.current_user().id
        except Exception as e:

            current_app.logger.debug(e)
            return bad_request(str(e))
        else:

            order = Order.create(**data)
            current_app.logger.debug("CREATED order: {}".format(order.to_dict()))
            return json_response(order.to_dict(), 201)
    else:

        return bad_request("Order already exists")

    
#update
@api_bp.route('/orders/<int:id>', methods=['PUT'])
@token_auth.login_required
def update_item(id):
    order = Order.get(id)
    
    if order:

        confirmed_order = ConfirmedOrder.get(id)
        if order.buyer_id == basic_auth.current_user().id:

            if confirmed_order:

                return bad_request("Order already confirmed")
            else:

                try:

                    data = json_request(['product_id','offer'], False)
                    data['buyer_id'] = order.buyer_id
                except Exception as e:

                    current_app.logger.debug(e)
                    return bad_request(str(e))
                else:

                    order.update(**data)
                    current_app.logger.debug("UPDATED order: {}".format(order.to_dict()))
                    return json_response(order.to_dict())
        else:

            return forbidden_access("You are not the buyer in this offer")
    else:

        current_app.logger.debug("Order {} not found".format(id))
        return not_found("Item not found")
    
    
# Delete order
@api_bp.route('/orders/<int:id>', methods=['DELETE'])
@token_auth.login_required 
def delete_item(id):

    order = Order.get(id)
    if order:

        confirmed_order = ConfirmedOrder.get(id)
        if order.buyer_id == basic_auth.current_user().id:

            if confirmed_order:

                return bad_request("Order already confirmed")
            else:

                order.delete()
                current_app.logger.debug("DELETED item: {}".format(id))
                return json_response(order.to_dict())
        else:

            return forbidden_access("You are not the owner of this product")
    else:

        current_app.logger.debug("Item {} not found".format(id))
        return not_found("Item not found")

@api_bp.route('/orders/<int:order_id>/confirmed', methods=['POST'])
@token_auth.login_required
def accept_order(order_id):
    order = Order.query.get(order_id)

    if order:
        if token_auth.current_user().id != order.product.seller_id:
            return jsonify(
                {
                    'error': 'Unauthorized', 
                    'message': 'You are not authorized to confirm this order', 
                    'success': False
                }), 401

        if order.confirmed_order:
            return jsonify(
                {
                    'error': 'Bad Request', 
                    'message': 'Order already confirmed',
                    'success': False
                }), 400

        confirmed_order = ConfirmedOrder(order=order)
        
        try:
            confirmed_order.save()
        except:
            return jsonify(
                {
                    'error': 'Bad Request', 
                    'message': 'Error confirming the order', 
                    'success': False
                }), 400

        current_app.logger.debug(f"Order {order_id} confirmed successfully")
        return jsonify(
            {
                'message': f'Order {order_id} confirmed successfully', 
                'success': True
            }), 200
    else:
        return not_found('Order not found')



@api_bp.route('/orders/<int:order_id>/confirmed', methods=['DELETE'])
@token_auth.login_required
def cancel_confirmed_order(order_id):
    confirmed_order = ConfirmedOrder.query.get(order_id)

    if confirmed_order:
        # Verificar si el usuario autenticado es el "seller" del producto asociado
        if token_auth.current_user().id != confirmed_order.order.product.seller_id:
            return jsonify(
                {
                    'error': 'Unauthorized', 
                    'message': 'You are not authorized to cancel this confirmed order', 
                    'success': False
                }), 401

        try:
            confirmed_order.delete()
        except:
            return jsonify(
                {
                    'error': 'Bad Request', 
                    'message': 'Error cancelling the confirmed order', 
                    'success': False
                }), 400

        current_app.logger.debug(f"ConfirmedOrder {order_id} cancelled successfully")
        return jsonify(
            {
                'message': f'ConfirmedOrder {order_id} cancelled successfully', 
                'success': True
            }), 200
    else:
        return not_found('ConfirmedOrder not found')
    


