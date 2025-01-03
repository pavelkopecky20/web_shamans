from flask import Flask
from extensions import db, mail
from routes.main_routes import bp as main_routes  # Import blueprintu

app = Flask(__name__)

app.config.from_object('config.Config')  # Načte konfiguraci

# Inicializace rozšíření
db.init_app(app)
mail.init_app(app)

# Registrace blueprintu
app.register_blueprint(main_routes)

if __name__ == '__main__':
    app.run(debug=True)
