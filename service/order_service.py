from . import db, base_response, jsonify
from validation.order_validation import CreateOrderValidation, QueryOrderValidation, UpdateOrderValidation
from models.order import Order
from models.pruduct import Product
from marshmallow import ValidationError

def create_order_service(request_data: dict, admin_id: int) -> dict:
    try:
        data = CreateOrderValidation().load(request_data)
        find_product = Product.query.filter_by(id=data['product_id'], deleted_at=None).first()
        if find_product is None:
            return jsonify(base_response.response_failed(404, 'failed', 'Product not found')), 404
        
        total_price = data['total_amount'] * find_product.price
        order = Order(admin_id=admin_id, product_id=data['product_id'], total_amount=data['total_amount'], total_price=total_price)
        db.session.add(order)
        db.session.commit()
        return jsonify(base_response.response_success(201, 'success', order.to_dict())), 201
    except ValidationError as err:
        return jsonify(base_response.response_failed(400, 'failed', err.messages)), 400
    except Exception as err:
        print(f'some error: {err}')
        return jsonify(base_response.response_failed(500, 'failed', 'Internal Server Error')), 500
    
def get_all_order_service(start_date: str, end_date: str) -> dict:
    try:
        data = QueryOrderValidation().load({'start_date': start_date, 'end_date': end_date})
        if start_date and end_date:
            orders = Order.query.filter(Order.created_at.between(data['start_date'], data['end_date']), Order.deleted_at == None).all()
        else:
            orders = Order.query.filter_by(deleted_at=None).all()
        return jsonify(base_response.response_success(200, 'success', [order.to_dict() for order in orders])), 200
    except ValidationError as err:
        return jsonify(base_response.response_failed(400, 'failed', err.messages)), 400
    except Exception as err:
        print(f'some error: {err}')
        return jsonify(base_response.response_failed(500, 'failed', 'Internal Server Error')), 500
    
def get_order_by_id_service(order_id: int) -> dict:
    try:
        order = Order.query.filter_by(id=order_id, deleted_at=None).first()
        if order is None:
            return jsonify(base_response.response_failed(404, 'failed', 'Order not found')), 404
        return jsonify(base_response.response_success(200, 'success', order.to_dict())), 200
    except Exception as err:
        print(f'some error: {err}')
        return jsonify(base_response.response_failed(500, 'failed', 'Internal Server Error')), 500

def update_order_service(order_id: int, request_data: dict, admin_id: int) -> dict:
    try:
        data = UpdateOrderValidation().load(request_data)
        order = Order.query.filter_by(id=order_id, deleted_at=None).first()
        if order is None:
            return jsonify(base_response.response_failed(404, 'failed', 'Order not found')), 404
        
        find_product = Product.query.filter_by(id=data['product_id'], deleted_at=None).first()
        if find_product is None:
            return jsonify(base_response.response_failed(404, 'failed', 'Product not found')), 404
        
        order.total_amount = data['total_amount']
        order.product_id = data['product_id']
        order.admin_id = admin_id
        order.total_price = order.total_amount * find_product.price
        db.session.commit()
        return jsonify(base_response.response_success(200, 'success', order.to_dict())), 200
    except ValidationError as err:
        return jsonify(base_response.response_failed(400, 'failed', err.messages)), 400
    except Exception as err:
        print(f'some error: {err}')
        return jsonify(base_response.response_failed(500, 'failed', 'Internal Server Error')), 500
    
def delete_order_service(order_id: int) -> dict:
    try:
        order = Order.query.filter_by(id=order_id, deleted_at=None).first()
        if order is None:
            return jsonify(base_response.response_failed(404, 'failed', 'Order not found')), 404
        order.deleted_at = True
        db.session.commit()
        return jsonify(base_response.response_success(200, 'success', order.to_dict())), 200
    except Exception as err:
        print(f'some error: {err}')
        return jsonify(base_response.response_failed(500, 'failed', 'Internal Server Error')), 500