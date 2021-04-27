from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Length, Email, EqualTo

class RecoverPasswordForm(FlaskForm): # class RegisterForm extends FlaskForm
  email = StringField('Email',validators=[InputRequired(),Length(max=50),Email(message='Invalid email')])
  password = PasswordField('Password',validators=[InputRequired(),Length(min=6,max=80)])
  confirm_password = PasswordField('Repeat Password', validators=[EqualTo('password',message='Passwords must match')])


class RegisterForm(FlaskForm): # class RegisterForm extends FlaskForm
    email = StringField('Email',validators=[InputRequired(),Length(max=50),
                                            Email(message='Invalid email')])
    username = StringField('User Name',validators=[InputRequired(),Length(min=4,max=15)])
    password = PasswordField('Password',validators=[InputRequired(),Length(min=6,max=80)])
    confirm_password = PasswordField('Repeat Password',
                                     validators=[EqualTo('password',
                                                         message='Passwords must match')])

class LoginForm(FlaskForm): # class RegisterForm extends FlaskForm
    emailORusername = StringField('User name or Email',validators=[InputRequired()])
    password = PasswordField('Password',validators=[InputRequired()])
    remember = BooleanField('Remember me')


class ProfileForm(FlaskForm): # class RegisterForm extends FlaskForm
    email = StringField('Email')
    username = StringField('User Name')
    profile = StringField('Profile')