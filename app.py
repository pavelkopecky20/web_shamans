from flask import Flask
from flask_mail import Mail
from models import db
from routes import main_routes, admin_routes, contact_routes
from dotenv import load_dotenv
import os

load_dotenv()  # Načtení proměnných z .env
  
# Inicializace globálního objektu Mail
mail = Mail()

# Globální inicializace Mail
mail = Mail()

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')  # Načtení konfigurace

    # Inicializace databáze a Flask-Mail
    db.init_app(app)
    mail.init_app(app)

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


# dodělat:
# na index.html zobrazovat jen 2 řádky novinek, čtěte více...