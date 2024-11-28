from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mail import Mail, Message
from datetime import datetime
import json
import os
from models import db, Concert, News, About



def create_app():
    app = Flask(__name__) 
    app.secret_key = os.getenv('SECRET_KEY', 'your_secret_key_12345*')  # Použije proměnnou prostředí, pokud je nastavena
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///your_database.db'  # Cesta k vaší databázi
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    # Inicializace SQLAlchemy s aplikací
    db.init_app(app)
    # Konfigurace pro Flask-Mail
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USERNAME'] = 'band.shamans@gmail.com'
    app.config['MAIL_PASSWORD'] = 'TheShamans_1234*'
    mail = Mail(app)
    # Inicializace databáze při spuštění aplikace
    with app.app_context():
        db.create_all()  # Vytvoření tabulek
    return app

app = create_app()


# TOTO BYLO JEN PRO VYZKOUŠENÍ, ZDA SE PŘIDÁVÁ DO DB.
# # Otevření kontextu aplikace
# with app.app_context():
#     # Vložení koncertu do databáze
#     new_concert = Concert(
#         date=datetime(2024, 11, 20).date(),
#         time=datetime(2024, 11, 20, 19, 30).time(),
#         venue='Městská hala',
#         event_link='https://example.com'
#     )
#     db.session.add(new_concert)
#     db.session.commit()


    
   # přepsáno - původně z json, nyní to tahá z db 
def load_concerts():
    loaded_concerts = Concert.query.all()
    return loaded_concerts    
    
def get_upcoming_concert():
    today = datetime.now().date()
    upcoming_concert = Concert.query.filter(Concert.date >= today).order_by(Concert.date).first()
    
    if upcoming_concert:
        # Přidáme formátované datum pro šablonu
        month_mapping = {
            1: 'leden', 2: 'únor', 3: 'březen', 4: 'duben',
            5: 'květen', 6: 'červen', 7: 'červenec', 8: 'srpen',
            9: 'září', 10: 'říjen', 11: 'listopad', 12: 'prosinec'
        }
        formatted_date = f"{upcoming_concert.date.day}. {month_mapping[upcoming_concert.date.month]}"
        return {
            'formatted_date': formatted_date,
            'venue': upcoming_concert.venue,
            'event_link': upcoming_concert.event_link
        }
    return None


# def get_upcoming_concert():
#     band_concerts = load_concerts()  # Načtení koncertů ze souboru    
    
#     # Mapa anglických názvů měsíců na české
#     month_mapping = {
#         'January': 'leden',
#         'February': 'únor',
#         'March': 'březen',
#         'April': 'duben',
#         'May': 'květen',
#         'June': 'červen',
#         'July': 'červenec',
#         'August': 'srpen',
#         'September': 'září',
#         'October': 'říjen',
#         'November': 'listopad',
#         'December': 'prosinec',
#     }

#     # Seřadit koncerty podle datumu
#     sorted_concerts = sorted(band_concerts, key=lambda x: datetime.strptime(x['date'], '%Y-%m-%d').date())
#     today = datetime.now().date()

#     # Procházení seznamu koncertů
#     for concert in sorted_concerts:
#         concert_date = datetime.strptime(concert['date'], '%Y-%m-%d').date()
#         if concert_date >= today:
#             # Přidání formátovaného data k informacím o koncertu
#             day = concert_date.day  # Získání dne bez formátování
#             month = concert_date.strftime('%B')  # Měsíc v anglickém formátu
#             month_czech = month_mapping[month]  # Převod měsíce na český formát
#             concert['formatted_date'] = f'{day}. {month_czech}'  # Např. '4. října'
#             return concert
#     return None


# administrace pro přidávání nových koncertů
@app.route('/admin/add_concert', methods=['GET', 'POST'])
def add_concert():
    if request.method == 'POST':
        # Získání dat z formuláře
        date = request.form['date']
        time = request.form['time']
        venue = request.form['venue']
        event_link = request.form['event_link']
        
        # Vytvoření a uložení nového koncertu do databáze
        new_concert = Concert(date=date, time=time, venue=venue, event_link=event_link)

        new_concert.date = datetime.strptime(new_concert.date, '%Y-%m-%d').date()
        new_concert.time = datetime.strptime(new_concert.time, '%H:%M').time()  # Pokud `time` je zadáno jako text

        db.session.add(new_concert)
        db.session.commit()
        flash('Koncert byl úspěšně přidán!')
        return redirect(url_for('concerts'))  # přesměrování na stránku s koncerty

    return render_template('add_concert.html')

# NAHRAZENO TÍM, CO JE DOLE -  def edit_news(id) A def admin_news()
# # administrace pro přidávání nových novinek
# @app.route('/admin/add_news', methods=['GET', 'POST'])
# def add_news():
#     if request.method == 'POST':
#         title = request.form['title']
#         content = request.form['content']
        
#         news = News(title=title, content=content)   # přidání do db
#         db.session.add(news)
#         db.session.commit()
#         flash("Novinka byla úspěšně přidána.")
#         return redirect(url_for('news'))      
#     return render_template('add_news.html')  

# načtení novinek ze souboru news_band.json  - předěláné na načtení z db - SQLAlchemy
# def load_band_news():
#     with open("news_band.json", "r", encoding='utf-8') as file:
#         return json.load(file)

def load_band_news():           # předělané - načítá z db. Načte všechny novinky
    loaded_news = News.query.order_by(News.id_news.desc()).all()     # aby byly ve správném pořadí - ta poslední nahoře
    print(loaded_news)
    return loaded_news   

# Výpis aktuální novinky na stránku index.html  
def get_latest_new():
    latest_new = load_band_news()[0]  # Načteme poslední novinku
    # PŮVODNĚ TO BYL SLOVNÍK, KDYŽ TO TAHALO Z JSON. TEĎ JE TO OBJEKT 
    # for key, value in latest_new():
    #     # Omezíme text na přibližně 3 řádky (např. 200 znaků jako příklad)
    #     limited_text = value[:200] + '...' if len(value) > 200 else value  # Přidáme '...' pokud je text delší
    #     return {key: limited_text}  # Vrátíme jako slovník, např. {'titulek': 'text...'}

    limited_text = latest_new.content[:200] + '...' if len(latest_new.content) > 200 else latest_new.content    # Omezí text na 200 znaků
    return {'title': latest_new.title, 'content': limited_text}



# Výpis všech novinek na stránku news.html
def get_all_news():
    all_news = load_band_news()
    return all_news

# přidávání about - administrace a uložení do db. Podobně jako u novinek
@app.route('/admin/add_about', methods=['GET', 'POST'])
def add_about():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        
        about_entry = About(title=title, content=content)  # Vytvoříme novou instanci třídy About
        db.session.add(about_entry)
        db.session.commit()
        flash("Informace o kapele byly úspěšně přidány.")
        return redirect(url_for('about'))  # Přesměrování na stránku About
        
    return render_template('add_about.html')  # Vykreslíme formulář

# funkce pro volání about
def get_about():
    loaded_about = About.query.all()
    return loaded_about

@app.route('/')
def index():
    upcoming_concert = get_upcoming_concert()
    news_homepage = get_latest_new()
    return render_template('index.html', upcoming_concert=upcoming_concert, news_homepage=news_homepage)


@app.route('/news')
def news():
    get_news = get_all_news() 
    return render_template('news.html', get_news=get_news)

@app.route('/about')
def about():
    about_info = get_about()        #  About.query.first() šlo by i napřímo bez funkce - Načteme první záznam, nebo uprav, pokud chceš více záznamů
    return render_template('about.html', about_info=about_info)


@app.route('/concerts')
def concerts():
    band_concerts = load_concerts()  # Načtení koncertů ze souboru
    return render_template('concerts.html', concerts=band_concerts)


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']
        
        msg = Message('Message from ' + name,
                      sender=email,
                      recipients=['your_email@gmail.com'])
        msg.body = message
        mail.send(msg)
        flash('Your message has been sent!')
        return redirect(url_for('contact'))
    return render_template('contact.html')

@app.route('/gallery')
def gallery():
    # Získání seznamu všech obrázků z adresáře static/images/gallery
    image_folder = os.path.join(app.static_folder, 'images', 'gallery')
    images = [f for f in os.listdir(image_folder) if f.endswith(('jpg', 'jpeg', 'png', 'gif'))]
    
    return render_template('gallery.html', images=images)




# ÚPRAVA NOVINKY i EDITACE


@app.route('/admin/news', methods=['GET', 'POST'])
def admin_news():
    # Přidání nové novinky
    if request.method == 'POST' and 'add_news' in request.form:
        title = request.form['title']
        content = request.form['content']
        new_news = News(title=title, content=content)
        db.session.add(new_news)
        db.session.commit()
        return redirect(url_for('admin_news'))

    # Načtení všech novinek pro zobrazení
    news_list = News.query.order_by(News.date_posted.desc()).all()

    return render_template('admin_news.html', news_list=news_list)

@app.route('/admin/news/edit/<int:id>', methods=['POST'])
def edit_news(id_news):
    news_item = News.query.get_or_404(id_news)

    # Aktualizace existující novinky
    news_item.title = request.form[f'title_{id}']
    news_item.content = request.form[f'content_{id}']
    db.session.commit()

    return redirect(url_for('admin_news'))




if __name__ == '__main__':
    app.run(debug=True)

# dodělat rozdělení koncertů na aktuální - odehrané
# dodělat úpravu novinek a about a koncertů https://chatgpt.com/c/66f2b07d-463c-8008-8ec2-a5ad00b4c80c