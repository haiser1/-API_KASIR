from flask import request
from middleware.jwt_auth import token_required
from service.product_service import create_product_service, delete_product_service, get_all_product_service, get_product_by_id_service, update_product_service

@token_required
def create_product_controller(current_user):
    request_data = request.get_json()
    response_data = create_product_service(request_data)
    return response_data

@token_required
def get_all_product_controller(current_user):
    response_data = get_all_product_service()
    return response_data

@token_required
def get_product_by_id_controller(current_user, product_id):
    response_data = get_product_by_id_service(product_id)
    return response_data

@token_required
def update_product_controller(current_user, product_id):
    request_data = request.get_json()
    response_data = update_product_service(product_id, request_data)
    return response_data

@token_required
def delete_product_controller(current_user, product_id):
    response_data = delete_product_service(product_id)
    return response_data