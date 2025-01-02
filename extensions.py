# pro účely emailu. Zabrání cirkulárnímu importu

from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy

mail = Mail()
db = SQLAlchemy()
