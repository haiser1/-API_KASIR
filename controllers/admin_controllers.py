from flask import request
from service.admin_service import get_current_admin_service
from middleware.jwt_auth import token_required

@token_required
def get_current_admin_controller(current_user: dict) -> dict:
    response_data = get_current_admin_service(current_user['id'])
    return response_data