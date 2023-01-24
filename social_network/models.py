from flask_login import UserMixin
from datetime import datetime
from social_network import db, app, login_manager

# Funcion con decorador(por convencion es .user_loader) para recargar al usuario desde el user.id guardado en la sesion
# Esta funcion espera 4 atributos de la clase, que se los daremos con UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)
    
    def __repr__(self):
        return f'User {self.username}, {self.email}, {self.image_file}'


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False,default=datetime.utcnow)
    content = db.Column(db.Text(144), nullable=False)
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id'), nullable=False)
    
    def __repr__(self):
        return f'Publicacion {self.title}, {self.date_posted}'
    
    
# Creacion de tablas en base de datos

db.init_app(app)
with app.app_context():
    db.create_all()