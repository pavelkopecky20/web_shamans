from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_migrate import Migrate

db = SQLAlchemy()


def create_app_db():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///your_database.db'  # Zde upravte cestu k databázi
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)  # Zaregistrujte SQLAlchemy s aplikací

    # Další konfigurace nebo registrace modrých tisků, pokud je potřeba
    
    with app.app_context():
        db.create_all()  # Vytvoří tabulky, pokud ještě neexistují

    return app

# Definice modelů
class Concert(db.Model):
    id_concert = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    time = db.Column(db.Time, nullable=True)
    venue = db.Column(db.String(100), nullable=False)
    event_link = db.Column(db.String(255), nullable=True)
    is_past = db.Column(db.Boolean, default=False)  # Zda koncert již proběhl

class News(db.Model):
    id_news = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    date_posted = db.Column(db.DateTime, default=datetime.utcnow)

class About(db.Model):
    id_about = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f'<About {self.title}>'

# Vytvoření aplikace
app = create_app_db()




if __name__ == '__main__':
    app.run(debug=True)
