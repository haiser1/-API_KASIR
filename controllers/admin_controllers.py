from flask import request
from service.admin_service import get_current_admin_service, get_all_admin_service, update_cuurrent_admin_service, update_admin_by_sup_admin_service, delete_admin_by_sup_admin_service
from middleware.jwt_auth import token_required, super_admin_required

@token_required
def get_current_admin_controller(current_user: dict) -> dict:
    response_data = get_current_admin_service(current_user['id'])
    return response_data

@super_admin_required
def get_all_admin_controller(current_user) -> dict:
    response_data = get_all_admin_service()
    return response_data

@token_required
def update_current_admin_controller(current_user):
    request_data = request.get_json()
    response_data = update_cuurrent_admin_service(current_user['id'], request_data)
    return response_data

@super_admin_required
def update_admin_by_sup_admin_controller(current_user, admin_id):
    request_data = request.get_json()
    response_data = update_admin_by_sup_admin_service(admin_id, request_data)
    return response_data

@super_admin_required
def delete_admin_by_sup_admin_controller(current_user, admin_id):
    response_data = delete_admin_by_sup_admin_service(admin_id)
    return response_data