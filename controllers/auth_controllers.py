from flask import request
from service.auth_service import register_admin_service, login_admin_service
from middleware.jwt_auth import super_admin_required

@super_admin_required
def register_admin_controller(current_user) -> dict:
    request_data = request.get_json()
    response_data = register_admin_service(request_data)
    return response_data
    
def login_admin_controller() -> dict:
    request_data = request.get_json()
    response_data = login_admin_service(request_data)
    return response_data