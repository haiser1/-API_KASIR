from . import ma
from marshmallow import fields

class CreteCategoryValidation(ma.Schema):
    name = fields.String(required=True)

class UpdateCategoryValidation(ma.Schema):
    name = fields.String(required=False)
