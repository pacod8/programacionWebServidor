from flask import Blueprint, render_template, abort, flash, redirect, url_for, request
from flask_login import login_required, current_user
from sqlalchemy import or_, and_
from models import get_db, User, Course, Follow, ParticipationCode, ParticipationRedeem, CourseTasks, CourseTaskAttemps, UserFile
import random

from module003.forms import *

module003 = Blueprint("module003", __name__,static_folder="static",template_folder="templates")
db = get_db()

@module003.route('/')
def module003_index():
    return render_template("module003_index.html", module='module003')

@module003.route('/tasks' ,methods=['GET', 'POST'])
def module003_tasks():
    form = TaskForm()
    courses = Course.query.filter_by(user_id=current_user.id).all()
    tasks = CourseTasks.query.filter(CourseTasks.id.in_(list(map(lambda x: x.id, courses))))
    for course in Course.query.filter_by(user_id=current_user.id):
        form.course_id.choices += [(course.id,  str(course.id) + ' - ' + course.institution_name + ' - ' + course.name)]
    
    if request.method == 'POST':
        if form.validate_on_submit():
            if not form.id.data:
                task = CourseTasks(name=form.name.data.strip(),
                            description=form.description.data.strip(),
                            course_id=form.course_id.data,
                            date_limit=form.date_limit.data )
                db.session.add(task)
                db.session.commit()
                try:
                    db.session.commit()
                    flash("Task created successfully")
                except:
                    db.session.rollback()
                    flash("Error creating task!")
            else:
                change = 0
                task = CourseTasks.query.get(form.id.data)
                newtaskname = form.name.data.strip()
                if task.name != newtaskname:
                    task.name = newtaskname
                    change = 1

                newdescription = form.description.data.strip()
                if task.description != newdescription:
                    task.description = newdescription
                    change = 1

                newcourse = form.course_id.data.strip()
                if task.course_id != newcourse:
                    task.course_id = newcourse
                    change = 1

                newdate = form.date_limit.data
                if task.date_limit != newdate:
                    task.date_limit = newdate
                    change = 1

                try:
                    if change:
                        db.session.commit()
                        flash("Task updated successfully!")
                    else:
                        flash("Nothing has changed!")
                except:
                    db.session.rollback()
                    flash("Error updating task!")
                return redirect(url_for('module003.module003_tasks'))

    elif ('rowid' in request.args):
        task = CourseTasks.query.get(request.args['rowid'])
        course = Course.query.filter_by(id=task.course_id).first()
        if not task or not course or course.user_id != current_user.id:
            flash('Error retrieving data for the task {}'.format(request.args['rowid']))
        else:
            form = TaskForm(id=task.id, name=task.name, description=task.description, course_id= task.course_id, date_limit=task.date_limit)

    courses = Course.query.filter_by(user_id=current_user.id).all()
    tasks = CourseTasks.query.filter(CourseTasks.id.in_(list(map(lambda x: x.id, courses)))).order_by(CourseTasks.course_id).all()
    for course in Course.query.filter_by(user_id=current_user.id):
        form.course_id.choices += [(course.id,  str(course.id) + ' - ' + course.institution_name + ' - ' + course.name)]
    for t in tasks:
        course = list(filter(lambda x: x.id == t.course_id, courses))[0]
        t.course_name = str(course.id) + ' - ' + course.institution_name + ' - ' + course.name
    return render_template("module003_tasks.html",module="module003", form=form, rows=tasks)


@module003.route('/attempt')
def module003_attempt():
    return render_template("module003_attempt.html", module='module003')
