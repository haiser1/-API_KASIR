from flask import request
from service.category_service import create_category_service, get_all_category_service, get_category_by_id_service, update_category_service, delete_category_service
from middleware.jwt_auth import token_required

@token_required
def create_category_controller(current_user):
    request_data = request.get_json()
    response_data = create_category_service(request_data)
    return response_data

@token_required
def get_all_category_controller(current_user):
    response_data = get_all_category_service()
    return response_data

@token_required
def get_category_by_id_controller(current_user, category_id):
    response_data = get_category_by_id_service(category_id)
    return response_data
@token_required
def update_category_controller(current_user, category_id):
    request_data = request.get_json()
    response_data = update_category_service(category_id, request_data)
    return response_data

@token_required
def delete_category_controller(current_user, category_id):
    response_data = delete_category_service(category_id)
    return response_data