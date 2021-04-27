
from application import get_app
from flask_login import login_required, login_user, logout_user, current_user
from flask import render_template, request, redirect, url_for, flash
from sqlalchemy import or_
from models import User, get_db
from werkzeug.security import generate_password_hash, check_password_hash
from mail import send_email
app = get_app()
db = get_db()

from forms import *

@app.route('/profile',methods=['GET','POST'])
@login_required
def profile():
    form = ProfileForm(email=current_user.email,
                       username=current_user.username,
                       profile=current_user.profile)
    return render_template("profile.html",module="profile", form=form)


@app.route('/login',methods=['GET','POST'])
def login():
    form = LoginForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            user = User.query.filter(or_(User.email==form.emailORusername.data,
                                         User.username==form.emailORusername.data)).first()
            if not user or not check_password_hash(user.password, form.password.data):
                flash("Wrong user or Password!")
            elif user.confirmed:
                login_user(user, remember=form.remember.data)
                flash("Welcome back {}".format(current_user.username))
                return redirect(url_for('dashboard'))
            else:
                flash("User not confirmed. Please visit your email to confirm your user.")


    return render_template('login.html',module="login", form=form)

import random
@app.route('/signup',methods=['GET','POST'])
def signup():
    form = RegisterForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            # Ejercicio - juntar la dos partes!!! Coger del formulario y meter en base de datos!
            try:
                password_hashed=generate_password_hash(form.password.data,method="sha256")
                newuser = User(email=form.email.data,
                               username=form.username.data,
                               userhash=str(random.getrandbits(128)),
                               password=password_hashed)
                db.session.add(newuser)
                db.session.commit()
                send_email(newuser.email,'Please, confirm email / Por favor, confirmar correo.','mail/new_user',user=newuser,url=request.host, newpassword=password_hashed)
                flash("Great, your user was created successfully please visit your email {} to confirm your email / Muy bien, ahora visite su correo electrónico {} para confirmar el correo.".format(newuser.email,newuser.email))
                return redirect(url_for('login'))
            except:
                db.session.rollback()
                flash("Error creating user!")
    return render_template('signup.html',module="signup", form=form)
# CONTROLLER - END

@app.route('/confirmuser/<username>/<userhash>/',methods=['GET'])
def confirmuser(username,userhash):
    user = User.query.filter_by(username=username).first()
    if not user:
        flash('Invalid url.')
    elif userhash != user.userhash:
        flash('Invalid url.')
    elif user.confirmed:
        flash('Url already used.')
    else:
        try:
            flash('User confirmed successfully.')
            user.confirmed = 1
            db.session.commit()
        except:
            db.session.rollback()
            flash("Error confirming user!")
    return redirect(url_for('login'))

@app.route('/changepassword',methods=['GET','POST'])
def changepassword():
  form = RecoverPasswordForm()
  if request.method == 'POST':
      if form.validate_on_submit():
          user = User.query.filter_by(email=form.email.data).first()
          if not user:
              flash('Email does not exist')
          else:
              password_hashed=generate_password_hash(form.password.data,method="sha256")
              send_email(user.email, 'Please confirm password change/ porfavor confiarmar cambio','mail/new_password', user=user,url=request.host,newpassword=password_hashed)
              flash('Great, pleas visit your emial and confirm passowrd change')
              return redirect(url_for('login'))
  return render_template('changepassword.html',module="login", form=form)



@app.route('/confirmpassword/<username>/<userhash>/<newpassword>/',methods=['GET'])
def confirmpassword(username,userhash,newpassword):
    user = User.query.filter_by(username=username).first()
    if not user:
        flash('Invalid url.')
    elif userhash != user.userhash:
        flash('Invalid url.')
    elif user.password == newpassword:
        flash('Url already used.')
    else:
        try:
            user.password == newpassword
            db.session.commit()
            flash('Password succesfullly changed')
        except:
            db.session.rollback()
            flash('Error changing password!')
    return redirect(url_for('login'))



@app.route('/logout')
@login_required
def logout():
    flash("See you soon {}".format(current_user.username))
    logout_user()
    return redirect(url_for('index'))


@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html',module="home")


@app.route('/')
def index():
    return render_template('index.html',module="home")


@app.errorhandler(500)
def internal_server_error(e):
    db.session.rollback()
    return render_template("500.html"), 500

@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404

@app.errorhandler(403)
def access_denied(e):
    return render_template("403.html"), 403