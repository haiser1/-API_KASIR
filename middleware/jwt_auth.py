from flask import request, jsonify
from functools import wraps
import jwt
from config import JWT_SECRET_KEY
from base.base_response import BaseResponse

base_response = BaseResponse()



def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify(base_response.response_failed(401, 'Unauthorized', 'Token is missing!')), 401
        token = token.split(" ")[1]
        if not token:
            return jsonify(base_response.response_failed(401, 'Unauthorized', 'Token is missing!')), 401
        try:
            data = jwt.decode(token, str(JWT_SECRET_KEY), algorithms=['HS256'])
            current_user = data 
        except jwt.ExpiredSignatureError:
            return jsonify(base_response.response_failed(401, 'Unauthorized', 'Token has expired!')), 401
        except jwt.InvalidTokenError:
            return jsonify(base_response.response_failed(401, 'Unauthorized', 'Token is invalid!')), 401
        return f(current_user, *args, **kwargs)
    return decorated

def super_admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify(base_response.response_failed(401, 'Unauthorized', 'Token is missing!')), 401
        token = token.split(" ")[1]
        if not token:
            return jsonify(base_response.response_failed(401, 'Unauthorized', 'Token is missing!')), 401
        try:
            data = jwt.decode(token, str(JWT_SECRET_KEY), algorithms=['HS256'])
            current_user = data 
        except jwt.ExpiredSignatureError:
            return jsonify(base_response.response_failed(401, 'Unauthorized', 'Token is expired!')), 401
        except jwt.InvalidTokenError:
            return jsonify(base_response.response_failed(401, 'Unauthorized', 'Token is invalid!')), 401
        if current_user['role'] != 'super_admin':
            return jsonify(base_response.response_failed(403, 'Forbidden', 'You are not authorized to access this resource!')), 403
        return f(current_user, *args, **kwargs)
    return decorated
