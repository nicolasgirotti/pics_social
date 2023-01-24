from flask_wtf import FlaskForm
from flask_login import current_user
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from social_network.models import User



class RegistrationForm(FlaskForm):
    username = StringField('Nombre de usuario', 
                           validators=[DataRequired(), Length(min=2, max=20)])
    
    email = StringField('Email', 
                           validators=[DataRequired(), Email()])
    
    password = PasswordField('Contraseña', 
                             validators=[DataRequired()])
        
    """
    Agregar al campo password expresion regular
    
    password = PasswordField('Contraseña', validators=[DataRequired(),
                                                       Regexp(
            r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{6,}$',
            message='La contraseña debe tener al menos 6 caracteres y contener al menos una letra mayúscula, una minúscula, un símbolo y un número'
        )])
    """
    confirm_password = PasswordField('Confirmar contraseña',
                                     validators=[DataRequired(), EqualTo('password')])
    
    submit = SubmitField('Registrarse')
    
    # Verificacion para que el usuario sea unico
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        
        if user:
            raise ValidationError('Ese usuario ya existe, elige otro por favor.')
    
    # Verificacion de que el email no exista en la base de datos
    def validate_email(self, email):
        email = User.query.filter_by(email=email.data).first()
        
        if email:
            raise ValidationError('Ese email ya se encuentra registrado, elige otro por favor.')
    
    
    
class LoginForm(FlaskForm):
    
    email = StringField('Email', 
                        validators=[DataRequired(), Email()])
    
    password = PasswordField('Contraseña', 
                            validators=[DataRequired()])
    
    remember = BooleanField('Recordarme')
    
    submit = SubmitField('Iniciar sesion')
    
    

class UpdateAccountForm(FlaskForm):
    username = StringField('Nombre de usuario',
                           validators=[Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[Email()])
    picture = FileField('Seleccionar foto de perfil', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Actualizar')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('El nombre de usuario ya existe, elija otro por favor')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('El email ya ha sido registrado, use otro por favor.')