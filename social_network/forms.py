from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo



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
    
    
class LoginForm(FlaskForm):
    
    email = StringField('Email', 
                        validators=[DataRequired(), Email()])
    
    password = PasswordField('Contraseña', 
                            validators=[DataRequired()])
    
    remember = BooleanField('Recordarme')
    
    submit = SubmitField('Iniciar sesion')
    
    
    