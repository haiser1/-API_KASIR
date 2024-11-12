from flask_marshmallow import Marshmallow
from marshmallow import fields, validate
from . import ma

class UpdateCurrentAdminValidation(ma.Schema):
    username = fields.String(required=False)
    email = fields.Email(required=False)
    old_password = fields.String(required=False)
    new_password = fields.String(required=False)

class UpdateAdminBySupAdminValidation(ma.Schema):
    username = fields.String(required=False)
    email = fields.Email(required=False)
    old_password = fields.String(required=False)
    new_password = fields.String(required=False)
    role = fields.String(required=False, validate=validate.OneOf(['super_admin', 'admin'], error="Invalid role. Choose either 'super_admin' or 'admin'"))