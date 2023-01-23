from flask import Flask, render_template, redirect, url_for, flash
from forms import RegistrationForm, LoginForm


app = Flask(__name__)

app.config['SECRET_KEY'] = 'a8a54e926a2b165d16413935e650936f'



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