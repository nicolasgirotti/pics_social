from flask import render_template, redirect, url_for, flash, request, abort
from PIL import Image
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.utils import secure_filename
from os import remove
from social_network import app, db, bcrypt
from social_network.forms import RegistrationForm, LoginForm, UpdateAccountForm, NewPost
from social_network.models import User, Post
import os, secrets, uuid


app.config['UPLOAD_FOLDER'] = 'UPLOAD_FOLDER'

@app.route("/", methods=['GET','POST'])
def home():
    page = request.args.get('page', 1, type=int)
    posts =  Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template('index.html', title='Red social', posts=posts)


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn




@app.route("/account", methods=['GET','POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Tu cuenta ha sido actualizada!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account',
                           image_file=image_file, form=form)

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
            return redirect(url_for('home'))
        else:
            flash('Inicio de sesion fallido. Comprueba tus datos', 'danger')
    return render_template('login.html', title='Iniciar sesion', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('login'))



# Rutas para publicaciones
def save_photo(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/UPLOAD_FOLDER', picture_fn)
    output_size = (350, 350)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    
    return picture_fn





@app.route("/post", methods=['GET', 'POST'])
@login_required
def new_post():
    
    form = NewPost()
    if form.validate_on_submit():
        image = form.photo.data
        image_path = save_photo(image)
        # Intentar modificar el path de la imagen con la funcion creada para guardar foto de perfil.
        post = Post(content=form.content.data, image=image_path, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Publicacion creada con exito', 'success')
        return redirect(url_for('home'))
    return render_template('new_post.html', title='Nueva publicacion',form=form)



@app.route("/post/<int:post_id>/delete", methods=['GET','POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if current_user.id != post.user_id:
        abort(404)
    db.session.delete(post)
    db.session.commit()
    if post.image:
        remove(app.root_path + '/static/UPLOAD_FOLDER/'+ post.image)
    
    return redirect(url_for('home'))



