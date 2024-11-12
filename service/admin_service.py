from models.admin import Admin
from flask import jsonify
from . import base_response

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