from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey
from flask_bcrypt import Bcrypt


app = Flask(__name__)

app.config['SECRET_KEY'] = 'a8a54e926a2b165d16413935e650936f'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy()

bcrypt = Bcrypt(app)

login_manager = LoginManager(app)

# Le aclaramos a login_manager donde esta ubicada la ruta de inicio de sesion
login_manager.login_view = 'login'

# Categoria para el mensaje flash
login_manager.login_message_category = 'info'

from social_network import routes