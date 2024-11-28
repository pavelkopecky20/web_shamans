# routy jednotlivých hlavních stránek

from flask import Blueprint, render_template
from models import Concert, News, About

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    upcoming_concert = Concert.query.order_by(Concert.date).first()
    latest_news = News.query.order_by(News.date_posted.desc()).first()
    return render_template('index.html', concert=upcoming_concert, news=latest_news)

@bp.route('/news')
def news():
    news_list = News.query.order_by(News.date_posted.desc()).all()
    return render_template('news.html', news_list=news_list)

@bp.route('/about')
def about():
    about_info = About.query.all()
    return render_template('about.html', about=about_info)
