from flask import Flask
from flask_mail import Mail
from models import db
from routes import main_routes, admin_routes, contact_routes

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')  # Načtení konfigurace
    db.init_app(app)
    Mail(app)

    with app.app_context():
        db.create_all()  # Inicializace databáze

    # Registrace blueprintů
    app.register_blueprint(main_routes.bp)
    app.register_blueprint(admin_routes.bp, url_prefix='/admin')
    app.register_blueprint(contact_routes.bp)

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
