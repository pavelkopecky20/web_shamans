# routy pro administraci

from flask import Blueprint, render_template, request, redirect, url_for, flash
from models import db, News, Concert

bp = Blueprint('admin', __name__)

@bp.route('/news', methods=['GET', 'POST'])
def admin_news():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        new_news = News(title=title, content=content)
        db.session.add(new_news)
        db.session.commit()
        flash("Novinka přidána.")
        return redirect(url_for('admin.admin_news'))
    news_list = News.query.order_by(News.date_posted.desc()).all()
    return render_template('admin_news.html', news_list=news_list)
