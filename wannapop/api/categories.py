from . import api_bp
from .errors import not_found, bad_request
from .. import db_manager as db
from ..models import Category, Product
from ..helper_json import json_request, json_response
from flask import current_app, jsonify

@api_bp.route('/categories', methods=['GET'])
def get_categories():
    categoria = Category.get_all()
    data = Category.to_dict_collection(categoria)
    return jsonify(
            {
                'data': data, 
                'success': True
            }), 200 
