from flask import Blueprint
from controllers.auth_controllers import register_admin_controller, login_admin_controller

auth_bp = Blueprint('auth_bp', __name__)

auth_bp.route('/api/admin/register', methods=['POST'])(register_admin_controller)
auth_bp.route('/api/admin/login', methods=['POST'])(login_admin_controller)