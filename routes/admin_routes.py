# http://127.0.0.1:5000/admin/news - TADY SE EDITUJE
# http://127.0.0.1:5000/admin/news/edit/1 - pokud víme id novinky (z databáze), můžeme ji přímo editovat i tady
 

from flask import Blueprint, render_template, request, redirect, url_for, flash
from models import db, News, Concert

bp = Blueprint('admin', __name__)

@bp.route('/news', methods=['GET', 'POST'])
def admin_news():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        if not title or not content:
            flash("Prosím vyplňte všechny údaje.")
            return redirect(url_for('admin.admin_news'))
        new_news = News(title=title, content=content)
        db.session.add(new_news)
        db.session.commit()
        flash("Novinka přidána.")
        return redirect(url_for('admin.admin_news'))
    news_list = News.query.order_by(News.date_posted.desc()).all()
    return render_template('admin_news.html', news_list=news_list)


@bp.route('/news/edit/<int:id>', methods=['POST'])
def edit_news(id):
    news = News.query.get_or_404(id)
    title = request.form.get('title')
    content = request.form.get('content')
    if not title or not content:
        flash("Nadpis a obsah jsou povinné!", "error")
        return redirect(url_for('admin.admin_news'))
    news.title = title
    news.content = content
    db.session.commit()
    flash("Novinka byla upravena.", "success")
    return redirect(url_for('admin.admin_news'))
