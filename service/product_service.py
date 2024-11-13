import datetime
from . import db, base_response, jsonify
from models.pruduct import Product
from models.category import Category
from marshmallow import ValidationError
from validation.product_validation import CreateProductValidation, UpdateProductValidation


def create_product_service(request_data: dict) -> dict:
    try:
        data = CreateProductValidation().load(request_data)
        product = Product.query.filter_by(name=data['name'], deleted_at=None).first()
        if product is not None:
            return jsonify(base_response.response_failed(400, 'failed', 'Product already exist')), 400
        find_category = Category.query.filter_by(id=data['category_id'], deleted_at=None).first()
        if find_category is None:
            return jsonify(base_response.response_failed(404, 'failed', 'Category not found')), 404
        product = Product(name=data['name'], price=data['price'], stock=data['stock'], category_id=data['category_id'])
        db.session.add(product)
        db.session.commit()
        return jsonify(base_response.response_success(201, 'success', product.to_dict())), 201
    except ValidationError as err:
        return jsonify(base_response.response_failed(400, 'failed', err.messages)), 400
    except Exception as err:
        print(f'some error: {err}')
        return jsonify(base_response.response_failed(500, 'failed', 'Internal Server Error')), 500
    
def get_all_product_service() -> dict:
    try:
        products = Product.query.filter_by(deleted_at=None).all()
        return jsonify(base_response.response_success(200, 'success', [product.to_dict() for product in products])), 200
    except Exception as err:
        print(f'some error: {err}')
        return jsonify(base_response.response_failed(500, 'failed', 'Internal Server Error')), 500

def get_product_by_id_service(product_id: int) -> dict:
    try:
        product = Product.query.filter_by(id=product_id, deleted_at=None).first()
        if product is None:
            return jsonify(base_response.response_failed(404, 'failed', 'Product not found')), 404
        return jsonify(base_response.response_success(200, 'success', product.to_dict())), 200
    except Exception as err:
        print(f'some error: {err}')
        return jsonify(base_response.response_failed(500, 'failed', 'Internal Server Error')), 500

def update_product_service(product_id: int, request_data: dict) -> dict:
    try:
        data = UpdateProductValidation().load(request_data)
        product = Product.query.filter_by(id=product_id, deleted_at=None).first()
        if product is None:
            return jsonify(base_response.response_failed(404, 'failed', 'Product not found')), 404
        find_category = Category.query.filter_by(id=data['category_id'], deleted_at=None).first()
        if find_category is None:
            return jsonify(base_response.response_failed(404, 'failed', 'Category not found')), 404
        product.name = data['name']
        product.price = data['price']
        product.stock = data['stock']
        product.category_id = data['category_id']
        db.session.commit()
        return jsonify(base_response.response_success(200, 'success', product.to_dict())), 200
    except ValidationError as err:
        return jsonify(base_response.response_failed(400, 'failed', err.messages)), 400
    except Exception as err:
        print(f'some error: {err}')
        return jsonify(base_response.response_failed(500, 'failed', 'Internal Server Error')), 500

def delete_product_service(product_id: int) -> dict:
    try:
        product = Product.query.filter_by(id=product_id, deleted_at=None).first()
        if product is None:
            return jsonify(base_response.response_failed(404, 'failed', 'Product not found')), 404
        product.deleted_at = datetime.datetime.now()
        db.session.commit()
        return jsonify(base_response.response_success(200, 'Product Successfully Deleted', 'Null')), 200
    except Exception as err:
        print(f'some error: {err}')
        return jsonify(base_response.response_failed(500, 'failed', 'Internal Server Error')), 500
