from flask import Blueprint, render_template, abort, flash, redirect, url_for, request
from flask_login import login_required, current_user
from models import get_db, Course
import random

from module001.forms import *

module001 = Blueprint("module001", __name__,static_folder="static",template_folder="templates")
db = get_db()

@module001.route('/')
@login_required
def module001_index():
    if current_user.profile in ('admin','staff','student'):
        return render_template("module001_index.html",module="module001")
    else:
        flash("Access denied!")
        return redirect(url_for('index'))


@module001.route('/course', methods=['GET','POST'])
@login_required
def module001_course():
    form = CourseForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            if not form.id.data:
                course = Course(name=form.name.data.strip(),
                                institution_name = form.institution_name.data.strip(),
                                user_id=current_user.id)
                db.session.add(course)
                db.session.commit()
                course.code = 'C'+str(course.id)+''.join(random.choice('AILNOQVBCDEFGHJKMPRSTUXZ') for i in range(4))
                newname = form.name.data.strip().replace('-' + course.code,'')
                if '-' + course.code not in newname:
                    course.name = newname + '-' + course.code
                db.session.commit()
                flash("Course created successfully with code: {}".format(course.code))
            else: # EJERCICIO - IMPLEMENTAR EL UPDATE DE institution_name y name - HASTA LAS 13:25
                pass
    elif ('rowid' in request.args):
        course = Course.query.get(request.args['rowid'])
        if not course or course.user_id != current_user.id:
            flash('Error retrieving data for the course {}'.format(request.args['rowid']))
        else:
            form = CourseForm(id=course.id, name=course.name.replace('-' + course.code,''), institution_name = course.institution_name, code=course.code)

    courses = Course.query.filter_by(user_id=current_user.id)
    return render_template("module001_course.html",module="module001", form=form, rows=courses)

@module001.route('/test')
def module001_test():
    return 'OK'