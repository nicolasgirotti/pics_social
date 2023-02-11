from time import localtime, strftime
from flask import render_template, redirect, url_for, flash, request, abort
from PIL import Image
from flask_login import login_user, logout_user, current_user, login_required
from flask_mail import Message
from flask_socketio import send, join_room, leave_room
from os import remove
from social_network import app, db, bcrypt, mail, socketio
from social_network.forms import (RegistrationForm, LoginForm, UpdateAccountForm, 
                                  NewPost, ResetPassword,ResetRequest)
from social_network.models import User, Post
import os, secrets, bleach


ROOMS = ['pics grupal']


# Carpeta donde se guardan las fotos de las publicaciones 
app.config['UPLOAD_FOLDER'] = 'UPLOAD_FOLDER'


# Error de pagina
@app.errorhandler(404)
def page_not_found_404(error):
    return render_template('error.html', error=error), 404


@app.errorhandler(500)
def page_not_found_500(error):
    return render_template('error.html',error=error), 500


# Rutas relacionadas al registro de cuentas

@app.route("/registration", methods=['GET', 'POST'])
def registration():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=(form.username.data).lower(), email=(form.email.data).lower(), password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Cuenta creada, puedes iniciar sesion.', 'info')
        return redirect(url_for('login'))
    return render_template('registration.html', title='Registro de usuarios',form=form)



@app.route("/", methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    
    form = LoginForm()  
    if form.validate_on_submit():
        user = User.query.filter_by(email=(form.email.data).lower()).first()
        
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            flash('Has iniciado sesion', 'info')
            return redirect(url_for('home'))
        else:
            flash('Inicio de sesion fallido. Comprueba tus datos', 'danger')
            
    return render_template('login.html', title='Iniciar sesion', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route("/home", methods=['GET','POST'])
def home():
    # Query que obtiene la pagina, establece una pagina por defecto y valida el numero de paginas como enteros
    page = request.args.get('page', 1, type=int)
    # Estas deben ser las fotos del explorador. Agregar opcion compartir historia. Cuanta gente la leyo
    posts =  Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    user_photos = User.query.all()
    return render_template('index.html', title='Red social', posts=posts, user_photos=user_photos)


# Funcion para guardar la foto de perfil del usuario
def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)
    output_size = (300, 300)
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
        flash('Tu cuenta ha sido actualizada!', 'info')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account',
                           image_file=image_file, form=form)


@app.route("/profile/<string:username>")
@login_required
def profile(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    photos = Post.query.filter_by(author=user)\
        .order_by(Post.date_posted.desc())\
        .paginate(page=page, per_page=5)

    
    return render_template('profile.html', photos=photos, user=user)




# Rutas para guardar fotos de publicaciones en carpeta
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
        image_path = save_photo(form.photo.data)
        print(image_path)
        post = Post(content=form.content.data, image=image_path, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Publicacion creada con exito', 'info')
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


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Solicitud de reestablecimiento de contraseña', 
                  sender='readyplayer.parziv@gmail.com', 
                  recipients=[user.email])
    msg.body = f'''Para reestablecer tu contraseña, visita el siguiente link: 
{url_for('reset_password', token=token, _external=True)}

Si usted no realizo esta solicitud, simplemente ignore este email y no habra cambios en su cuenta.

'''
    mail.send(msg)


# Ruta para solicitar reestablecimiento de contraseña
@app.route("/reset_request", methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = ResetRequest()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        try:
            send_reset_email(user)
        except:
            pass
        flash('Se ha enviado un correo con instrucciones para reestablecer su contraseña', 'info')
        return redirect(url_for('login'))
    return render_template('reset_request.html', title='Solicitar cambio de contraseña',form=form)


# Ruta para reestablecer una nueva contraseña
@app.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    user = User.verify_token(token)
    if user is None:
        flash('El tocken es invalido o el token ha expirado')
        return redirect(url_for('reset_request'))
    form = ResetPassword()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        user.password = hashed_password
        db.session.commit()
        return redirect(url_for('login'))
        
    return render_template('reset_password.html', title='Reestablecer contraseña',form=form, token=token)




# Rutas de follow

@app.route('/follow/<username>', methods=['GET', 'POST'])
@login_required
def follow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('Usuario invalido', 'danger')
        return redirect(url_for('profile', username=username))
    if current_user.is_following(user):
        flash(f'Ya estas siguiendo a {user.username}')
        return redirect(url_for('profile', username=username))
    current_user.follow(user)
    db.session.commit()
    flash(f'Has empezado a seguir a {user.username}.', 'info')
    return redirect(url_for('profile', username=username))



@app.route('/unfollow/<username>', methods=['GET', 'POST'])
@login_required
def unfollow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('Invalid user.')
        return redirect(url_for('profile', username=username))
    if not current_user.is_following(user):
        flash(f'Reformar ruta {user.username}.')
        return redirect(url_for('profile', username=username))
    current_user.unfollow(user)
    db.session.commit()
    flash(f'Has dejado de seguir a {user.username}', 'info')
    return redirect(url_for('profile', username=username))



# Logica de chat

@app.route("/chat", methods=['GET', 'POST'])
@login_required
def chat():
    return render_template('chat.html', username= current_user.username, rooms=ROOMS)

# Eventos

@socketio.on('join')
def join(data):
    
    join_room(data['room'])
    # Se envia una notificacion de que se unio cierto usuario, y se envia esta informacion
    # a cierto room.
    send({'msg': data['username'] + " se ha unido al chat de " + data['room'] }, room=data['room'])


@socketio.on('leave')
def leave(data):
    
    leave_room(data['room'])
    send({'msg': data['username'] + " ha abandonado el chat"}, room=data['room'])
    

@socketio.on('message')
def message(data):
    # Enviamos mensaje por broadcast a todos los clientes conectados
    send({'msg':bleach.clean(data['msg']), 'username':data['username'], 
          'time': strftime('%b-%d %I:%M%p', localtime())}, room=data['room'])
    
    
    
    
@app.route("/friends/<string:user>", methods=['GET', 'POST'])
def friends(user):
    user = User.query.filter_by(username=user).first()
    friends = user.friends()        
    return render_template('friends_list.html', friends=friends)
