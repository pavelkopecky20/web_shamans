from app import app  # Importuje aplikaci z app.py
from models import db, Concert, News
import json
from datetime import datetime

# def load_concerts():
#     with open('band_concerts.json', 'r', encoding='utf-8') as file:
#         return json.load(file)
    
# print(load_concerts())

def load_concerts():
    loaded_concerts = Concert.query.all()
    return loaded_concerts
    
 #   return loaded_concerts

    
# def get_upcoming_concert():
#     today = datetime.now().date()
#     upcoming_concert = Concert.query.filter(Concert.date >= today).order_by(Concert.date).first()
    
#     if upcoming_concert:
#         # Přidáme formátované datum pro šablonu
#         month_mapping = {
#             1: 'leden', 2: 'únor', 3: 'březen', 4: 'duben',
#             5: 'květen', 6: 'červen', 7: 'červenec', 8: 'srpen',
#             9: 'září', 10: 'říjen', 11: 'listopad', 12: 'prosinec'
#         }
#         formatted_date = f"{upcoming_concert.date.day}. {month_mapping[upcoming_concert.date.month]}"
#         return {
#             'formatted_date': formatted_date,
#             'venue': upcoming_concert.venue,
#             'event_link': upcoming_concert.event_link
#         }
#     return None

# Použijeme aplikaci v kontextu aplikace Flask
with app.app_context():
    print(load_concerts())
