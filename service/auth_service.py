import bcrypt
from config import db
from models.admin import Admin
from base.base_response import BaseResponse

base_response = BaseResponse()
def register_admin_service(username: str, email: str, password: str, role='super_admin') -> dict:
    if role not in ['super_admin', 'admin']:
        return base_response.response_failed(400, 'failed', 'Role must be super_admin or admin')
    admin = Admin.query.filter_by(email=email, deleted_at=None).first()
    if admin is not None:
        return base_response.response_failed(400, 'failed', 'Email already exists')
    password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    admin = Admin(username=username, email=email, password=password, role=role)
    db.session.add(admin)
    db.session.commit()
    
    return base_response.response_success(200, 'success', admin.to_dict())
