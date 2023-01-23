from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, current_user, login_required
from social_network import app, db, bcrypt
from social_network.forms import RegistrationForm, LoginForm
from social_network.models import User, Post


@app.route("/", methods=['GET','POST'])
def home():
    return render_template('index.html', title='Red social')


@app.route("/account", methods=['GET','POST'])
@login_required
def account():
    return render_template('account.html', title='Mi cuenta')

@app.route("/registration", methods=['GET', 'POST'])
def registration():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        # Generamos y guardamos la contraseña hasheada
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=(form.username.data).lower(), email=(form.email.data).lower(), password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Cuenta creada, puedes iniciar sesion.', 'success')
        return redirect(url_for('login'))
    return render_template('registration.html', title='Registro de usuarios',form=form)



@app.route("/login", methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()  
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            flash('Has iniciado sesion', 'success')
            # Para acceder a la pagina que visitamos sin estar loggeados
            next_page = request.referrer
            print(f"{next_page} next_page") 
            # Condicional ternario para redirigir a la pagina visitada 
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Inicio de sesion fallido. Comprueba tus datos', 'danger')
    return render_template('login.html', title='Iniciar sesion', form=form)



@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('login'))