from flask import Blueprint
from controllers.auth_controllers import register_admin_controller

auth_bp = Blueprint('auth_bp', __name__)

auth_bp.route('/api/admin/register', methods=['POST'])(register_admin_controller)