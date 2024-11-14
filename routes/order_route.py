from flask import Blueprint
from controllers.order_controllers import create_order_controller, get_all_order_controller, get_order_by_id_controller, update_order_controller, delete_order_controller

order_bp = Blueprint('order_bp', __name__)

order_bp.route('/api/orders', methods=['POST'])(create_order_controller)
order_bp.route('/api/orders', methods=['GET'])(get_all_order_controller)
order_bp.route('/api/orders/<int:order_id>', methods=['GET'])(get_order_by_id_controller)
order_bp.route('/api/orders/<int:order_id>', methods=['PUT'])(update_order_controller)
order_bp.route('/api/orders/<int:order_id>', methods=['DELETE'])(delete_order_controller)