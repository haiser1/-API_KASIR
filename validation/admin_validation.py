from flask_marshmallow import Marshmallow
from marshmallow import fields, validate
from . import ma

class UpdateAdminValidation(ma.Schema):
    username = fields.String(required=False)
    email = fields.Email(required=False)
    old_password = fields.String(required=False)
    new_password = fields.String(required=False, validate=validate.same_as("old_password"), error="Password doesn't match")
    role = fields.String(required=False, validate=validate.OneOf(["super_admin", "admin"], error="Invalid role. Choose either 'super_admin' or 'admin'"))
