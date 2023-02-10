from flask_login import UserMixin
import datetime
from social_network import db, app, login_manager
import jwt

# Funcion con decorador(por convencion es .user_loader) para recargar al usuario desde el user.id guardado en la sesion
# Esta funcion espera 4 atributos de la clase, que se los daremos con UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# Tabla auxiliar
class Follow(db.Model):
    __tablename__ = 'follows'
    follower_id = db.Column(db.Integer, db.ForeignKey('user.id'),
                            primary_key=True)
    followed_id = db.Column(db.Integer, db.ForeignKey('user.id'),
                            primary_key=True)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)
    
    followed = db.relationship('Follow',
                               foreign_keys=[Follow.follower_id],
                               backref=db.backref('follower', lazy='joined'),
                               lazy='dynamic',
                               cascade='all, delete-orphan')


    followers = db.relationship('Follow',
                                foreign_keys=[Follow.followed_id],
                                backref=db.backref('followed', lazy='joined'),
                                lazy='dynamic',
                                cascade='all, delete-orphan') 
    
    
    
    def __repr__(self):
        return f'User {self.username}, {self.email}, {self.image_file}'
    
    
    # Metodo para generar token
    def get_reset_token(self):
        token = jwt.encode({'user_id':self.id,'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)},app.config['SECRET_KEY'])
        
        return token
    
    # Metodo para verificar
    def verify_token(token):
        verify_token = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
        # Verifica dentro de bloque try except por si no es valido
        try:
            user_id = verify_token['user_id']
        except:
            return None
        # Si es valido, devuelve al usuario 
        return User.query.get(user_id)
    
    # Follow
    
    def is_following(self, user):
        if user.id is None:
            return False
        return self.followed.filter_by(
            followed_id=user.id).first() is not None
        
    def follow(self, user):
        if not self.is_following(user):
            f = Follow(follower=self, followed=user)
            db.session.add(f)
            return True
        
    def unfollow(self, user):
        f = self.followed.filter_by(followed_id=user.id).first()
        if f:
            db.session.delete(f)
            return True
        
        

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(60), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)
    image = db.Column(db.String(36))
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id'), nullable=False)
    
    def __repr__(self):
        return f'Publicacion {self.content}'




    
    



    


# Creacion de tablas en base de datos

db.init_app(app)
with app.app_context():
    db.create_all()