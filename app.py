from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail
from twilio.rest import Client

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'super secret key'
app.static_url_path = '/static'

app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = 'xxx'
app.config['MAIL_PASSWORD'] = 'xxx'
app.config['ADMINS'] = ['xxx@gmail.com']

db = SQLAlchemy(app)
mail = Mail(app)

auth_token = ''
account_sid = ''
client = Client(account_sid, auth_token)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
