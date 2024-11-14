import datetime
from . import db, base_response, jsonify
from validation.order_validation import CreateOrderValidation, QueryOrderValidation, UpdateOrderValidation
from models.order import Order
from models.pruduct import Product
from marshmallow import ValidationError

def create_order_service(request_data: list, admin: dict) -> dict:
    orders = []
    total_amount_price = 0
    for item in request_data:
        try:
            # Validasi setiap item menggunakan schema
            data = CreateOrderValidation().load(item)

            # Cek apakah produk ada dan belum dihapus
            find_product = Product.query.filter_by(id=data['product_id'], deleted_at=None).first()
            if find_product is None:
                return jsonify(base_response.response_failed(404, 'failed', 'Product not found')), 404
            
            # Hitung total harga
            if data['total_amount'] > find_product.stock:
                return jsonify(base_response.response_failed(400, 'failed', 'Stock not enough')), 400
            
            total_price = data['total_amount'] * find_product.price
            find_product.stock -= data['total_amount']
            total_amount_price += total_price
            
            # Buat objek order
            order = Order(admin_id=admin['id'], product_id=data['product_id'], total_amount=data['total_amount'], total_price=total_price)
            db.session.add(order)
            db.session.commit()
            orders.append(order.to_dict())
        
        except ValidationError as err:
            db.session.rollback()
            return jsonify(base_response.response_failed(400, 'failed', err.messages)), 400
        except Exception as err:
            db.session.rollback()
            print(f'some error: {err}')
            return jsonify(base_response.response_failed(500, 'failed', 'Internal Server Error')), 500

    return jsonify(base_response.response_success(201, 'success', {
        'orders': orders, 
        'admin_id': admin['id'],
        'admin_username': admin['username'],
        'total_amount_price': total_amount_price,
        'order_date': datetime.datetime.now()
        })), 201
    
def get_all_order_service() -> dict:
    try:
        orders = Order.query.filter_by(deleted_at=None).all()
        return jsonify(base_response.response_success(200, 'success', [order.to_dict_full() for order in orders])), 200
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
        return jsonify(base_response.response_success(200, 'success', order.to_dict_full())), 200
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
        return jsonify(base_response.response_success(200, 'success', order.to_dict_full())), 200
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