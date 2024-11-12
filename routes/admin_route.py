from flask import Blueprint
from controllers.admin_controllers import get_current_admin_controller, get_all_admin_controller

admin_bp = Blueprint('admin_bp', __name__)

admin_bp.route('/api/admin/current', methods=['GET'])(get_current_admin_controller)
admin_bp.route('/api/admin', methods=['GET'])(get_all_admin_controller)