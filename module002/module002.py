from flask import Blueprint, render_template, abort, flash, redirect, url_for, request

from flask_login import login_required, current_user
from sqlalchemy import or_, and_
from models import get_db, User, Course, Follow, ParticipationCode, ParticipationRedeem, PostComments
from sqlalchemy import asc
from .forms import *
import datetime

module002 = Blueprint("module002", __name__,static_folder="static",template_folder="templates")
db = get_db()

@module002.route('/', methods=["GET", "POST"])
@login_required
def module002_index():
    if current_user.profile in ('admin','staff','student'):
        cursos = Follow.query.filter(current_user.id==Follow.user_id)
        if cursos == None:
            flash("No sigues a ningun curso")


        return render_template('module002_index.html', cursos = cursos, module= 'module002')



    else:
        flash("Access denied!")
        return redirect(url_for('index'))

@module002.route('/post', methods=["GET", "POST"])
@login_required
def post_index():
    if current_user.profile in ('admin','staff','student'):

        course_id = request.args.get('id')
        form = PostForm()

        if form.validate_on_submit():
            post = PostComments(post=form.body.data,
                        user_id=current_user.id,
                        #user_id=1,
                        course_code = course_id,
                        date_created=datetime.datetime.now())
            try:
                db.session.add(post)
                db.session.commit()

            except:
                db.session.rollback()
                flash("Error posting!")

        posts = PostComments.query.filter(course_id == PostComments.course_code).order_by(asc(PostComments.date_created))
        users=[]
        for post in posts:
            users.append(User.query.filter_by(id=post.user_id).first())
            #user = [Ramon, Julia, sofia]

        return render_template('post_index.html', form=form, posts=posts, usernames = users, module= 'module002')#AÑADIR NOMBRE CURSO

    else:
        flash("Access denied!")
        return redirect(url_for('index'))




@module002.route('/test')
def module002_test():
    return 'OK'
