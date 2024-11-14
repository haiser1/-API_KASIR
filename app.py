from config import app, db
from routes.auth_route import auth_bp
from routes.admin_route import admin_bp
from routes.category_route import category_bp
from routes.product_route import product_bp
from routes.order_route import order_bp

app.register_blueprint(auth_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(category_bp)
app.register_blueprint(product_bp)
app.register_blueprint(order_bp)


if __name__ == '__main__':
    db.create_all()
    app.run(debug=True, port=5000)