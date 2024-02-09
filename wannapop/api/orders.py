from . import api_bp
from .errors import not_found, bad_request
from .. import db_manager as db
from ..models import Category, Product, Order, ConfirmedOrder
from ..helper_json import json_request, json_response
from flask import current_app, jsonify

@api_bp.route('/orders/<int:order_id>/confirmed', methods=['POST'])
def accept_order(order_id):
    order = Order.query.get(order_id)

    if order:
        if order.confirmed_order:
            return jsonify(
                {
                    'error': 'Bad Request', 
                    'message': 'Order ya esta confirmada',
                    'success': False
                }), 400

        confirmed_order = ConfirmedOrder(order=order)
        
        try:
            confirmed_order.save()
        except:
            return jsonify(
                {
                    'error': 'Bad Request', 
                    'message': 'Error al confirmar la order', 
                    'success': False
                }), 400

        current_app.logger.debug(f"Order {order_id} confirmada correctamente")
        return jsonify(
            {
                'Mensaje': f'Order {order_id} confirmada correctamente', 
                'success': True
            }), 200
    else:
        return not_found('Order no encontrada')


@api_bp.route('/orders/<int:order_id>/confirmed', methods=['DELETE'])
def cancel_confirmed_order(order_id):
    confirmed_order = ConfirmedOrder.query.get(order_id)

    if confirmed_order:
        try:
            confirmed_order.delete()
        except:
            return jsonify(
                {
                    'error': 'Bad Request', 
                    'message': 'Error al cancelar la confirmed order', 
                    'success': False
                }), 400

        current_app.logger.debug(f"ConfirmedOrder {order_id} cancelado correctamente")
        return jsonify(
            {
                'Mensaje': f'ConfirmedOrder {order_id} cancelado correctamente', 
                'success': True
            }), 200
    else:
        return not_found('ConfirmedOrder no encontrado')
