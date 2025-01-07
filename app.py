from flask import Flask
from extensions import db, mail
from routes.main_routes import bp as main_routes  # Import blueprintu hlavních stránek
from routes.admin_routes import bp as admin_routes  # Import blueprintu pro administraci

app = Flask(__name__)

app.config.from_object('config.Config')  # Načte konfiguraci

# Inicializace rozšíření
db.init_app(app)
mail.init_app(app)

# Registrace blueprintů
app.register_blueprint(main_routes)  # Registrace hlavního blueprintu
app.register_blueprint(admin_routes, url_prefix='/admin')  # Registrace admin blueprintu

if __name__ == '__main__':
    app.run(debug=True)
