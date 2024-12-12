from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()
    
class Concert(db.Model):
    id_concert = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    time = db.Column(db.Time, nullable=False)
    venue = db.Column(db.String(200), nullable=False)
    event_link = db.Column(db.String(200))

    @property
    def formatted_date(self):
        return self.date.strftime('%d.%m.%Y')  # Formátujte dle potřeby

class News(db.Model):
    id_news = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    date_posted = db.Column(db.DateTime, default=datetime.utcnow)
class About(db.Model):
    id_about = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
