from . import api_bp
from .errors import not_found, bad_request
from .. import db_manager as db
from ..models import Category, Product, Order, ConfirmedOrder
from ..helper_json import json_request, json_response
from flask import current_app, jsonify
from .helper_auth import token_auth

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

