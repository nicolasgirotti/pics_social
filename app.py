from flask import Flask, render_template, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey
from datetime import datetime
from forms import RegistrationForm, LoginForm


app = Flask(__name__)

app.config['SECRET_KEY'] = 'a8a54e926a2b165d16413935e650936f'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy()

class User(db.Model):
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

@app.route("/", methods=['GET','POST'])
def home():
    return render_template('index.html', title='Red social')

@app.route("/account", methods=['GET','POST'])
def account():
    return render_template('account.html', title='Mi cuenta')

@app.route("/registration", methods=['GET', 'POST'])
def registration():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash('Cuenta creada', 'success')
        return redirect(url_for('home'))
    return render_template('registration.html', title='Registro de usuarios',form=form)

@app.route("/login", methods=['GET','POST'])
def login():
    form = LoginForm()  
    if form.validate_on_submit():
        flash('Has iniciado sesion', 'success')
        return redirect(url_for('home'))
    return render_template('login.html', title='Iniciar sesion', form=form)



if __name__ == '__main__':
    app.run(debug=True)