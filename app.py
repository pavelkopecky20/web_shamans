from flask import Flask
from extensions import db, mail         # importují objekty db - SQLAlchemy a Flask Mail
from routes.main_routes import bp as main_routes  # Import blueprintu hlavních stránek
from routes.admin_routes import bp as admin_routes  # Import blueprintu pro administraci
from flask_migrate import Migrate

app = Flask(__name__)       # instance aplikace - __name__ umožní Flasku najít potřebné soubory 

app.config.from_object('config.Config')  # Načte konfiguraci. Objektu se předají údaje k db, tajné klíče atd.
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///instance/your_database.db'


# Inicializace rozšíření
db.init_app(app)            # aplikace se propojí s db
mail.init_app(app)          # umožní posílání emailů přímo z aplikace Flask-Mail

# Registrace blueprintů
app.register_blueprint(main_routes)  # Registrace hlavního blueprintu. Do aplikace se přidají main_routes
app.register_blueprint(admin_routes, url_prefix='/admin')  # Registrace admin blueprintu. Do aplilkace se přidají admin_routes. Všechny cesty budou s prefixem /admin

if __name__ == '__main__':  # spouští se přímo z tohoto souboru, ne odjinud
    app.run(debug=True)     # spouští apku s vývojovým režimem ladění

migrate = Migrate(app, db)

# Blueprinty umožní rozdělení aplikace na menší celky a jejich propojení. Lze je snadno importovat 
# Blueprint se do hlavní aplikce registruje metodou app.register_blueprint().

# Při požadavku na URL hledá Flask odpovídající funkci v blueprintech. Flask porovná cestu s blueprinty a zobrazí stránku 
# objekty db se importují přes admin_routes.py. Když se volají funkce, tak aplikace ví, že má pracovat s modely v db.