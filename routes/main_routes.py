# routy jednotlivých hlavních stránek - index, news, about, concerts, gallery

from flask import Blueprint, render_template
from models import Concert, News, About
import os
from datetime import datetime

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    concert = Concert.query.order_by(Concert.date).filter(Concert.date >= datetime.now().date()).first()
    news_homepage = News.query.order_by(News.date_posted.desc()).first()
    return render_template('index.html', concert=concert, news_homepage=news_homepage)

    
@bp.route('/news')
def news():
    news_list = News.query.order_by(News.date_posted.desc()).all()
    return render_template('news.html', news_list=news_list)

@bp.route('/about')
def about():
    about_info = About.query.all()
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