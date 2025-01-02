# http://127.0.0.1:5000/admin/news - TADY SE EDITUJE
# http://127.0.0.1:5000/admin/news/edit/1 - pokud víme id novinky (z databáze), můžeme ji přímo editovat i tady
 
# http://127.0.0.1:5000/admin/concerts/add  - koncerty
# http://127.0.0.1:5000/admin/about

from flask import Blueprint, render_template, request, redirect, url_for, flash
from models import db, News, Concert, About
from datetime import datetime

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

@bp.route('/concerts/add', methods=['GET', 'POST'])
def add_concert():
    if request.method == 'POST':
        try:
            # Získání hodnot z formuláře
            date = request.form.get('date')
            time = request.form.get('time')
            venue = request.form.get('venue')
            event_link = request.form.get('event_link')
            
            # Převod řetězců na objekty date a time
            date_obj = datetime.strptime(date, "%Y-%m-%d").date()
            time_obj = datetime.strptime(time, "%H:%M").time()
            
            # Kontrola, zda jsou všechna povinná pole vyplněná
            if not date_obj or not time_obj or not venue:
                flash("Prosím vyplňte všechny povinné údaje.")
                return redirect(url_for('admin.add_concert'))

            # Vytvoření nového koncertu
            new_concert = Concert(date=date_obj, time=time_obj, venue=venue, event_link=event_link)
            db.session.add(new_concert)
            db.session.commit()
            flash("Koncert byl úspěšně přidán.")
            return redirect(url_for('admin.add_concert'))
        
        except ValueError:
            flash("Špatný formát data nebo času.", "error")
            return redirect(url_for('admin.add_concert'))

    return render_template('add_concert.html')


@bp.route('/about', methods=['GET', 'POST'])
def admin_about():
    """
    Správa sekce About: přidávání a zobrazení článků.
    """
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        if not title or not content:
            flash("Prosím vyplňte všechny údaje.", "error")
            return redirect(url_for('admin.admin_about'))
        
        new_about = About(title=title, content=content)
        db.session.add(new_about)
        db.session.commit()
        flash("Článek o kapele byl úspěšně přidán.", "success")
        return redirect(url_for('admin.admin_about'))

    about_list = About.query.order_by(About.id_about.desc()).all()
    return render_template('add_about.html', about_list=about_list)


@bp.route('/about/edit/<int:id>', methods=['POST'])
def edit_about(id):
    """
    Úprava existujícího článku v sekci About.
    """
    about = About.query.get_or_404(id)
    title = request.form.get('title')
    content = request.form.get('content')
    if not title or not content:
        flash("Nadpis a obsah jsou povinné!", "error")
        return redirect(url_for('admin.admin_about'))
    
    about.title = title
    about.content = content
    db.session.commit()
    flash("Článek o kapele byl úspěšně upraven.", "success")
    return redirect(url_for('admin.admin_about'))
