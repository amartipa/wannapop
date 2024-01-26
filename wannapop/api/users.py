from . import api_bp
from .errors import not_found, bad_request
from ..models import User, BlockedUser
from ..helper_json import json_request, json_response
from flask import current_app