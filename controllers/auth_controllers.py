from flask import request, jsonify
from base.base_response import BaseResponse
from service.auth_service import register_admin_service

base_response = BaseResponse()
def register_admin_controller() -> dict:
    request_data = request.get_json()
    username = request_data['username']
    email = request_data['email']
    password = request_data['password']
    role = request_data['role']
    response_data = register_admin_service(username=username, email=email, password=password, role=role)
    return jsonify(response_data)
    
