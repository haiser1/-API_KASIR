from . import ma
from marshmallow import fields, validate

class CreateOrderValidation(ma.Schema):
    product_id = fields.Integer(required=True, validate=validate.Range(min=1, error="Product ID must be greater than 0"))
    total_amount = fields.Integer(required=True, validate=validate.Range(min=1, error="Total amount must be greater than 0"))
    
class QueryOrderValidation(ma.Schema):
    start_date = fields.Date(required=False)
    end_date = fields.Date(required=False)

class UpdateOrderValidation(ma.Schema):
    product_id = fields.Integer(required=True, validate=validate.Range(min=1, error="Product ID must be greater than 0"))
    total_amount = fields.Integer(required=True, validate=validate.Range(min=1, error="Total amount must be greater than 0"))