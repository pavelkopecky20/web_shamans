# routy pro odesílání emailů 

from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_mail import Message
from app import mail  # Import inicializovaného objektu mail

bp = Blueprint('contact', __name__)

@bp.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']

        # Vytvoření a odeslání e-mailu
        msg = Message(f"Message from {name}", sender=email, recipients=['your_email@gmail.com'])
        msg.body = message
        mail.send(msg)  # Použití inicializovaného objektu mail
        flash("Zpráva byla odeslána!")
        return redirect(url_for('contact.contact'))
    return render_template('contact.html')
