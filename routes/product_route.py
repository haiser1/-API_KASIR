from flask import Blueprint
from controllers.product_controllers import create_product_controller, get_all_product_controller, get_product_by_id_controller, update_product_controller, delete_product_controller

product_bp = Blueprint('product_bp', __name__)

product_bp.route('/api/products', methods=['POST'])(create_product_controller)
product_bp.route('/api/products', methods=['GET'])(get_all_product_controller)
product_bp.route('/api/products/<int:product_id>', methods=['GET'])(get_product_by_id_controller)
product_bp.route('/api/products/<int:product_id>', methods=['PUT'])(update_product_controller)
product_bp.route('/api/products/<int:product_id>', methods=['DELETE'])(delete_product_controller)