# app.py
from flask import Flask
from config import SECRET_KEY, SQLALCHEMY_DATABASE_URI
from models import db
from routes.admin import admin_bp

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = SECRET_KEY
    app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    app.register_blueprint(admin_bp)

    with app.app_context():
        db.create_all()
        # Initial admin user (for testing)
        from models import AdminUser
        from werkzeug.security import generate_password_hash
        if not AdminUser.query.first():
            hashed_password = generate_password_hash("admin", method='sha256')
            new_admin = AdminUser(username="admin", password=hashed_password)
            db.session.add(new_admin)
            db.session.commit()

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
