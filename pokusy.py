from app import app  # Importuje aplikaci z app.py
from models import db, Concert, News

# def load_concerts():
#     with open('band_concerts.json', 'r', encoding='utf-8') as file:
#         return json.load(file)
    
# print(load_concerts())

# def load_concerts():
#     loaded_concerts = Concert.query.all()
#     return loaded_concerts
    
def index():
   # concert = Concert.query.order_by(Concert.date).filter(Concert.date >= datetime.now().date()).first()
    news_homepage = News.query.order_by(News.date_posted.desc()).first()
    if len(news_homepage) <= 200:
        news_homepage_short = news_homepage 
        return(news_homepage_short)
    else:
        news_homepage_short = news_homepage[:200]   
        # read_more = read_more
        return(news_homepage_short)  
    
#    return render_template('index.html', concert=concert, news_homepage=news_homepage)

print(index())