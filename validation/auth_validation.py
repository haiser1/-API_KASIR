from flask_marshmallow import Marshmallow
from marshmallow import fields, validate
from config import app

ma = Marshmallow(app)

class RegisterValidation(ma.Schema):
    username = fields.String(required=True, validate=validate.Length(min=1, error="Username cannot be empty"))
    email = fields.Email(required=True, validate=validate.Length(min=1, error="Email cannot be empty"))
    password = fields.String(required=True, validate=validate.Length(min=1, error="Password cannot be empty"))
    role = fields.String(
        required=True,
        validate=[
            validate.Length(min=1, error="Role cannot be empty"),
            validate.OneOf(["super_admin", "admin"], error="Invalid role. Choose either 'super_admin' or 'admin'")
        ]
    )

class LoginValidation(ma.Schema):
    email = fields.Email(required=True, validate=validate.Length(min=1, error="Email cannot be empty"))
    password = fields.String(required=True, validate=validate.Length(min=1, error="Password cannot be empty"))