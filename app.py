from config import app, db
from routes.auth_route import auth_bp
from routes.admin_route import admin_bp
from routes.category_route import category_bp
from routes.product_route import product_bp
from routes.order_route import order_bp
from flask_cors import CORS
from flask_swagger_ui import get_swaggerui_blueprint

CORS(app)

SWAGGER_URL = '/api/docs'
API_URL = '/static/api_dock.yml'
swagger_ui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Kasir API Documentation"
    }
)
app.register_blueprint(swagger_ui_blueprint, url_prefix=SWAGGER_URL)

app.register_blueprint(auth_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(category_bp)
app.register_blueprint(product_bp)
app.register_blueprint(order_bp)


if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)