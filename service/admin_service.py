import bcrypt
from marshmallow import ValidationError
from models.admin import Admin
from flask import jsonify
from . import base_response, db
from validation.admin_validation import UpdateCurrentAdminValidation

def get_current_admin_service(admin_id: int) -> dict:
    try:
        admin = Admin.query.filter_by(id=admin_id, deleted_at=None).first()
        if admin is None:
            return jsonify(base_response.response_failed(400, 'failed', 'Admin not found')), 400
        return jsonify(base_response.response_success(200, 'success', admin.to_dict())), 200
    except Exception as err:
        print(f'some error: {err}')
        return jsonify(base_response.response_failed(500, 'failed', 'Internal Server Error')), 500

def get_all_admin_service() -> dict:
    try:
        admins = Admin.query.filter_by(deleted_at=None).all()
        return jsonify(base_response.response_success(200, 'success', [admin.to_dict() for admin in admins])), 200
    except Exception as err:
        print(f'some error: {err}')
        return jsonify(base_response.response_failed(500, 'failed', 'Internal Server Error')), 500
    
def update_cuurrent_admin_service(admin_id: int, request_data: dict) -> dict:
    try:
        UpdateCurrentAdminValidation().load(request_data)
        admin = Admin.query.filter_by(id=admin_id, deleted_at=None).first()
        if admin is None:
            return jsonify(base_response.response_failed(400, 'failed', 'Admin not found')), 400
        if 'username' in request_data and request_data['username'] != '':
            admin.username = request_data['username']
        if 'email' in request_data and request_data['email'] != '':
            admin.email = request_data['email']
        if 'new_password' in request_data and request_data['new_password'] != '':
            if 'old_password' not in request_data or request_data['old_password'] == '':
                return jsonify(base_response.response_failed(400, 'failed', 'Old password required')), 400
            match = bcrypt.checkpw(request_data['old_password'].encode('utf-8'), admin.password.encode('utf-8'))
            if not match:
                return jsonify(base_response.response_failed(400, 'failed', 'Old password invalid')), 400
            admin.password = bcrypt.hashpw(request_data['new_password'].encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        if 'role' in request_data and request_data['role'] != '':
            admin.role = request_data['role']
        if 'old_password' in request_data and request_data['old_password'] != '':
            match = bcrypt.checkpw(request_data['old_password'].encode('utf-8'), admin.password.encode('utf-8'))
            if not match:
                return jsonify(base_response.response_failed(400, 'failed', 'Old password invalid')), 400
        
        db.session.commit()
        return jsonify(base_response.response_success(200, 'success', admin.to_dict())), 200
    except ValidationError as err:
        return jsonify(base_response.response_failed(400, 'failed', err.messages)), 400
    except Exception as err:
        print(f'some error: {err}')
        return jsonify(base_response.response_failed(500, 'failed', 'Internal Server Error')), 500