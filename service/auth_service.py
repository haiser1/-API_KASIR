import bcrypt
from config import db, JWT_SECRET_KEY
from models.admin import Admin
from . import base_response
import jwt
from flask import jsonify
import datetime
from validation.auth_validation import LoginValidation, RegisterValidation
from marshmallow import ValidationError

def register_admin_service(request_data: dict) -> dict:
    try:
        data = RegisterValidation().load(request_data)
        admin = Admin.query.filter_by(email=data['email'], deleted_at=None).first()
        if admin is not None:
            return jsonify(base_response.response_failed(400, 'failed', 'Email already exist')), 400
        password = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        admin = Admin(username=data['username'], email=data['email'], password=password, role=data['role'])
        db.session.add(admin)
        db.session.commit()
        return jsonify(base_response.response_success(200, 'success', admin.to_dict())), 200
    except ValidationError as err:
        return jsonify(base_response.response_failed(400, 'failed', err.messages)), 400
    except Exception as err:
        print(f'some error: {err}')
        return jsonify(base_response.response_failed(500, 'failed', 'Internal Server Error')), 500
    
def login_admin_service(request_data: dict) -> dict:
    try:
        data = LoginValidation().load(request_data)
        email = data['email']
        password = data['password']
        admin = Admin.query.filter_by(email=email, deleted_at=None).first()
        if admin is None:
            return  jsonify(base_response.response_failed(400, 'failed', 'Email or password invalid')), 400
        if not bcrypt.checkpw(password.encode('utf-8'), admin.password.encode('utf-8')):
            return jsonify(base_response.response_failed(400, 'failed', 'Email or password invalid')), 400
        payload = {
            'email': admin.email,
            'id': admin.id,
            'role': admin.role,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=12)
        }
        token = jwt.encode(payload, JWT_SECRET_KEY, algorithm='HS256')
        return jsonify(base_response.response_success(200, 'success', token)), 200
    except ValidationError as err:
        return jsonify(base_response.response_failed(400, 'failed', err.messages)), 400
    except Exception as err:
        print(f'some error: {err}')
        return jsonify(base_response.response_failed(500, 'failed', 'Internal Server Error')), 500