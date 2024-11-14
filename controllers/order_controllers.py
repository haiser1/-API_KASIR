from flask import request
from service.order_service import create_order_service, delete_order_service, get_all_order_service, get_order_by_id_service, update_order_service
from middleware.jwt_auth import token_required

@token_required
def create_order_controller(current_user) -> dict:
    request_data = request.get_json()
    response_data = create_order_service(request_data, current_user)
    return response_data

@token_required
def get_all_order_controller(current_user) -> dict:
    response_data = get_all_order_service()
    return response_data

@token_required
def get_order_by_id_controller(current_user, order_id) -> dict:
    response_data = get_order_by_id_service(order_id)
    return response_data

@token_required
def update_order_controller(current_user, order_id) -> dict:
    request_data = request.get_json()
    response_data = update_order_service(order_id, request_data, current_user['id'])
    return response_data

@token_required
def delete_order_controller(current_user, order_id) -> dict:
    response_data = delete_order_service(order_id)
    return response_data