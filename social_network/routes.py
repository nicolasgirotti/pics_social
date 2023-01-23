from flask import render_template, redirect, url_for, flash
from social_network import app
from social_network.forms import RegistrationForm, LoginForm
from social_network.models import User, Post


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

