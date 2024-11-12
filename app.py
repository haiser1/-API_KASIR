from config import app, db
from routes.auth_route import auth_bp
from routes.admin_route import admin_bp

app.register_blueprint(auth_bp)
app.register_blueprint(admin_bp)



if __name__ == '__main__':
    db.create_all()
    app.run(debug=True, port=5000)