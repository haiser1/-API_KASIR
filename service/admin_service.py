import bcrypt
from marshmallow import ValidationError
from models.admin import Admin
from flask import jsonify
from . import base_response, db
from validation.admin_validation import UpdateCurrentAdminValidation, UpdateAdminBySupAdminValidation
import datetime

def get_current_admin_service(admin_id: int) -> dict:
    try:
        admin = Admin.query.filter_by(id=admin_id, deleted_at=None).first()
        if admin is None:
            return jsonify(base_response.response_failed(404, 'failed', 'Admin not found')), 404
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
        data = UpdateCurrentAdminValidation().load(request_data)
        admin = Admin.query.filter_by(id=admin_id, deleted_at=None).first()
        if admin is None:
            return jsonify(base_response.response_failed(404, 'failed', 'Admin not found')), 404
        if data.get('username'):
            admin.username = data['username']
        if data.get('email'):
            admin.email = data['email']
        if data.get('role'):
            admin.role = data['role']
        
        # Jika new_password diberikan, validasi old_password
        if data.get('new_password'):
            if not data.get('old_password'):
                return jsonify(base_response.response_failed(400, 'failed', 'Old password required')), 400
            if not bcrypt.checkpw(data['old_password'].encode('utf-8'), admin.password.encode('utf-8')):
                return jsonify(base_response.response_failed(400, 'failed', 'Old password invalid')), 400
            admin.password = bcrypt.hashpw(data['new_password'].encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        db.session.commit()
        
        return jsonify(base_response.response_success(200, 'success', admin.to_dict())), 200
    except ValidationError as err:
        return jsonify(base_response.response_failed(400, 'failed', err.messages)), 400
    except Exception as err:
        print(f'some error: {err}')
        return jsonify(base_response.response_failed(500, 'failed', 'Internal Server Error')), 500
    
def update_admin_by_sup_admin_service(admin_id: int, request_data: dict) -> dict:
    try:
        data = UpdateAdminBySupAdminValidation().load(request_data)
        admin = Admin.query.filter_by(id=admin_id, deleted_at=None).first()
        if admin is None:
            return jsonify(base_response.response_failed(404, 'failed', 'Admin not found')), 404
        if data.get('username'):
            admin.username = data['username']
        if data.get('email'):
            admin.email = data['email']
        if data.get('role'):
            admin.role = data['role']
        
        # Jika new_password diberikan, validasi old_password
        if data.get('new_password'):
            if not data.get('old_password'):
                return jsonify(base_response.response_failed(400, 'failed', 'Old password required')), 400
            if not bcrypt.checkpw(data['old_password'].encode('utf-8'), admin.password.encode('utf-8')):
                return jsonify(base_response.response_failed(400, 'failed', 'Old password invalid')), 400
            admin.password = bcrypt.hashpw(data['new_password'].encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        db.session.commit()
        
        return jsonify(base_response.response_success(200, 'success', admin.to_dict())), 200
    except ValidationError as err:
        return jsonify(base_response.response_failed(400, 'failed', err.messages)), 400
    except Exception as err:
        print(f'some error: {err}')
        return jsonify(base_response.response_failed(500, 'failed', 'Internal Server Error')), 500
    
def delete_admin_by_sup_admin_service(admin_id: int) -> dict:
    try:
        admin = Admin.query.filter_by(id=admin_id, deleted_at=None).first()
        if admin is None:
            return jsonify(base_response.response_failed(404, 'failed', 'Admin not found')), 404
        admin.deleted_at = datetime.datetime.now()
        db.session.commit()
        return jsonify(base_response.response_success(200, 'Admin Successfully Deleted', 'Null')), 200
    except Exception as err:
        print(f'some error: {err}')
        return jsonify(base_response.response_failed(500, 'failed', 'Internal Server Error')), 500