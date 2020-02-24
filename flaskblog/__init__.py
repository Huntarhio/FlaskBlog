from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import  Mail

app = Flask(__name__)
app.config['SECRET_KEY'] = 'd29e808cb25a8d4cc3f71ece460c433d'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'
app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'adeotiadegboyega@gmail.com'  #ensure to use environment variable in the future
app.config['MAIL_PASSWORD'] = 'crownboy'

mail = Mail(app)

from flaskblog import routes
from flaskblog.posts.routes import posts
from flaskblog.users.routes import users
from flaskblog.main.routes import main

app.register_blueprint(posts)
app.register_blueprint(users)
app.register_blueprint(main)
