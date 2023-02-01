from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey
from flask_bcrypt import Bcrypt
from flask_mail import Mail
import os


# Instancia de aplicacion
app = Flask(__name__)

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['RECAPTCHA_PUBLIC_KEY'] = os.getenv('RECAPTCHA_PUBLIC_KEY')

app.config['RECAPTCHA_PRIVATE_KEY'] = os.getenv('RECAPTCHA_PRIVATE_KEY')



# Instancia de base de datos
db = SQLAlchemy()

# Instancia para hashear contraseñas
bcrypt = Bcrypt(app)

# Instancia para el administrador de sesion
login_manager = LoginManager(app)

# Le aclaramos a login_manager donde esta ubicada la ruta de inicio de sesion
login_manager.login_view = 'login'

# Categoria para el mensaje flash
login_manager.login_message_category = 'info'


# Configuracion necesaria para enviar mails
app.config['MAIL_SERVER'] = 'smtp.gmail.com'

app.config['MAIL_PORT'] = 587

app.config['MAIL_USE_TLS'] = True

app.config['MAIL_USERNAME'] = os.getenv('EMAIL_ADDRESS')

app.config['MAIL_PASSWORD'] = os.getenv('EMAIL_PASSWORD')

# Instancia de Mail
mail = Mail(app)


from social_network import routes