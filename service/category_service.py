from . import db, base_response
from validation.category_validation import CreteCategoryValidation, UpdateCategoryValidation
from models.category import Category
from flask import jsonify
from marshmallow import ValidationError
import datetime

def create_category_service(request_data: dict) -> dict:
    try:
        data =CreteCategoryValidation().load(request_data)
        category = Category.query.filter_by(name=data['name'], deleted_at=None).first()
        if category is not None:
            return jsonify(base_response.response_failed(400, 'failed', 'Category already exist')), 400
        category = Category(name=data['name'])
        db.session.add(category)
        db.session.commit()
        return jsonify(base_response.response_success(201, 'success', category.to_dict())), 201
    except ValidationError as err:
        return jsonify(base_response.response_failed(400, 'failed', err.messages)), 400
    except Exception as err:
        print(f'some error: {err}')
        return jsonify(base_response.response_failed(500, 'failed', 'Internal Server Error')), 500
    
def get_all_category_service() -> dict:
    try:
        categories = Category.query.filter_by(deleted_at=None).all()
        return jsonify(base_response.response_success(200, 'success', [category.to_dict() for category in categories])), 200
    except Exception as err:
        print(f'some error: {err}')
        return jsonify(base_response.response_failed(500, 'failed', 'Internal Server Error')), 500

def get_category_by_id_service(category_id: int) -> dict:
    try:
        category = Category.query.filter_by(id=category_id, deleted_at=None).first()
        if category is None:
            return jsonify(base_response.response_failed(404, 'failed', 'Category not found')), 404
        return jsonify(base_response.response_success(200, 'success', category.to_dict())), 200
    except ValidationError as err:
        return jsonify(base_response.response_failed(400, 'failed', err.messages)), 400
    except Exception as err:
        print(f'some error: {err}')
        return jsonify(base_response.response_failed(500, 'failed', 'Internal Server Error')), 500
    
def update_category_service(category_id: int, request_data: dict) -> dict:
    try:
        data = UpdateCategoryValidation().load(request_data)
        category = Category.query.filter_by(id=category_id, deleted_at=None).first()
        if category is None:
            return jsonify(base_response.response_failed(404, 'failed', 'Category not found')), 404
        category.name = data['name']
        db.session.commit()
        return jsonify(base_response.response_success(200, 'success', category.to_dict())), 200
    except ValidationError as err:
        return jsonify(base_response.response_failed(400, 'failed', err.messages)), 400
    except Exception as err:
        print(f'some error: {err}')
        return jsonify(base_response.response_failed(500, 'failed', 'Internal Server Error')), 500
    
def delete_category_service(category_id: int) -> dict:
    try:
        category = Category.query.filter_by(id=category_id, deleted_at=None).first()
        if category is None:
            return jsonify(base_response.response_failed(404, 'failed', 'Category not found')), 404
        category.deleted_at = datetime.datetime.now()
        db.session.commit()
        return jsonify(base_response.response_success(200, 'Category Successfully Deleted', 'Null')), 200
    except Exception as err:
        print(f'some error: {err}')
        return jsonify(base_response.response_failed(500, 'failed', 'Internal Server Error')), 500