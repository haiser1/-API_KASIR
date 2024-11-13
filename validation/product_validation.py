from . import ma
from marshmallow import fields, validate


class CreateProductValidation(ma.Schema):
    name = fields.String(required=True, validate=validate.Length(min=1, error="Name cannot be empty"))
    price = fields.Float(required=True, validate=validate.Range(min=0, error="Price must be greater than or equal to 0"))
    stock = fields.Integer(required=True, validate=validate.Range(min=0, error="Stock must be greater than or equal to 0"))
    category_id = fields.Integer(required=True, validate=validate.Range(min=1, error="Category ID must be greater than 0"))

class UpdateProductValidation(ma.Schema):
    name = fields.String(required=True, validate=validate.Length(min=1, error="Name cannot be empty"))
    price = fields.Float(required=True, validate=validate.Range(min=0, error="Price must be greater than or equal to 0"))
    stock = fields.Integer(required=True, validate=validate.Range(min=0, error="Stock must be greater than or equal to 0"))
    category_id = fields.Integer(required=True, validate=validate.Range(min=1, error="Category ID must be greater than 0"))