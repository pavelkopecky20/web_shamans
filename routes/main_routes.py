# routy jednotlivých hlavních stránek - index, news, about, concerts, gallery

from flask import Blueprint, render_template
from models import Concert, News, About         # načtení objektů db
import os
from datetime import datetime

bp = Blueprint('main', __name__)    # objekt Blueprintu. __name__ říká Flasku, kde se mají hledat šablony a další statické soubory

@bp.route('/')          # adresa
def index():            # funkce se zavolá, když uživatel navštíví adresu
    concert = Concert.query.order_by(Concert.date).filter(Concert.date >= datetime.now().date()).first()    # dotaz na db - aktuální koncert
    news_homepage = News.query.order_by(News.date_posted.desc()).first()        # dotaz na db - aktuální novinka
    
    # Zkrácení textu na max. 200 znaků
    max_length = 200
    is_truncated = False        # zda byl text zprávy zkrácen 
    news_content = news_homepage.content

    if len(news_content) > max_length:
        news_content = news_content[:max_length] + "..."
        is_truncated = True     
    
    return render_template('index.html', concert=concert, news_homepage=news_homepage, news_content=news_content, 
        is_truncated=is_truncated)

    
@bp.route('/news')
def news():
    news_list = News.query.order_by(News.date_posted.desc()).all()
    return render_template('news.html', news_list=news_list)

@bp.route('/about')
def about():
    about_info = About.query.all()      # načte všechny články z tabulky About v db 
    return render_template('about.html', about=about_info)

@bp.route('/concerts')
def concerts():
#    concerts = Concert.query.all()
    concerts_new = Concert.query.order_by(Concert.date).filter(Concert.date >= datetime.now().date())
    concerts_old = Concert.query.order_by(Concert.date).filter(Concert.date < datetime.now().date())
    return render_template('concerts.html', concerts_new=concerts_new, concerts_old=concerts_old) 

@bp.route('/gallery')
def gallery():
    image_folder = os.path.join('static', 'images', 'gallery')
    images = [f for f in os.listdir(image_folder) if f.endswith(('jpg', 'jpeg', 'png', 'gif'))]   
    return render_template('gallery.html', images=images)

@bp.route('/contact')
def contact():
    return render_template('contact.html')

@bp.route('/video')
def video():
    return render_template('video.html')