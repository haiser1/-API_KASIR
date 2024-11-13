from flask import Blueprint
from controllers.category_controllers import create_category_controller, get_all_category_controller, get_category_by_id_controller, update_category_controller, delete_category_controller

category_bp = Blueprint('category_bp', __name__)

category_bp.route('/api/categories', methods=['POST'])(create_category_controller)
category_bp.route('/api/categories', methods=['GET'])(get_all_category_controller)
category_bp.route('/api/categories/<int:category_id>', methods=['GET'])(get_category_by_id_controller)
category_bp.route('/api/categories/<int:category_id>', methods=['PUT'])(update_category_controller)
category_bp.route('/api/categories/<int:category_id>', methods=['DELETE'])(delete_category_controller)