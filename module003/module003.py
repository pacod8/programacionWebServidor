from flask import Blueprint, render_template, abort, flash, redirect, url_for, request, current_app
from flask_login import login_required, current_user
from sqlalchemy import or_, and_
from models import get_db, User, Course, Follow, ParticipationCode, ParticipationRedeem, CourseTasks, CourseTaskAttemps, UserFile
import random
from werkzeug.utils import secure_filename
import os
import uuid

from module003.forms import *
from helpers import role_required, role_not_allowed

module003 = Blueprint("module003", __name__,static_folder="static",template_folder="templates")
db = get_db()

@module003.route('/')
@login_required
def module003_index():
    return render_template("module003_index.html", module='module003')

@module003.route('/tasks', methods=['GET', 'POST'])
@login_required
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
    tasks = CourseTasks.query.filter(CourseTasks.course_id.in_(list(map(lambda x: x.id, courses)))).order_by(CourseTasks.course_id).all()
    for course in Course.query.filter_by(user_id=current_user.id):
        form.course_id.choices += [(course.id,  str(course.id) + ' - ' + course.institution_name + ' - ' + course.name)]
    if len(courses) != 0:
        print(courses)
        for t in tasks:
            course = list(filter(lambda x: x.id == t.course_id, courses))[0]
            t.course_name = str(course.id) + ' - ' + course.institution_name + ' - ' + course.name
    return render_template("module003_tasks.html",module="module003", form=form, rows=tasks)

@module003.route('/attempt', methods=['GET', 'POST'])
@login_required
def module003_attempt():
    filter_form = TaskAttemptFilterForm()
    courses = Course.query.filter_by(user_id=current_user.id).all()
    filter_courses = list(map(lambda x: x.id, courses))

    tasks = CourseTasks.query.filter(CourseTasks.course_id.in_(filter_courses))
    filter_task = list(map(lambda x: x.id, tasks))
    for t in tasks:
        filter_form.task.choices += [(t.id, t.name)]

    if request.method == 'POST':
        if filter_form.validate_on_submit():
            filter_courses = [filter_form.task.data] if int(filter_form.task.data) != -1 else filter_task

    elif ('rowid' in request.args):
        pass

    attempts = CourseTaskAttemps.query.filter(CourseTaskAttemps.task_id.in_(filter_task))

    for a in attempts:
        task = list(filter(lambda x: x.id == a.task_id, tasks))[0]
        a.task_name = task.name
    return render_template("module003_attempt.html", module='module003', filter_form=filter_form, rows=attempts)


@module003.route('/attempt-detail', methods=['GET', 'POST'])
@login_required
def module003_attempt_detail(): #TODO checar si la tarea esta en un curso que siga el usuario
    form = TaskAttemptForm()

    if request.method == 'POST':
        if form.validate_on_submit():
            fileatt = None
            if (form.attachment.data):
                f = form.attachment.data
                filename = f.filename.split('.')
                filename.insert(-1, str(uuid.uuid4().hex))
                filename[0] = filename[0][:15]
                filename = secure_filename('.'.join(filename))
                f.save(os.path.join(current_app.config['UPLOADS_FOLDER'], filename))
                filetype = f.mimetype
                
                fileatt = UserFile(filename=filename, filetype=filetype, user_id=current_user.id)
                db.session.add(fileatt)
                db.session.commit()
            if(not form.id.data):
                # TODO: checkear que todo es del usuario
                attempt = CourseTaskAttemps(task_id=form.task_id.data, user_id=current_user.id,
                    comments=form.comments.data, attachment=fileatt.id if fileatt else None, grade=form.grade.data)
            else:
                attempt = CourseTaskAttemps.query.get(form.id.data)
                attempt.comments = form.comments.data
                attempt.attachments = fileatt.id if fileatt else None
                attempt.grade = form.grade.data
            db.session.add(attempt)
            db.session.commit()
            task = CourseTasks.query.filter_by(id=form.task_id.data).first()
            form.id.data = attempt.id

    elif ('taskid' in request.args):
        attempt = CourseTaskAttemps.query.filter_by(task_id=request.args['taskid']).first()
        task = CourseTasks.query.filter_by(id=request.args['taskid']).first()
        course = Course.query.filter_by(id=task.course_id).first()
        if not task or not course or course.user_id != current_user.id:#TODO: checar que si es usuario hace follow
            flash('Error retrieving data for the task {}'.format(request.args['taskid']))
            return redirect(url_for('module003.module003_tasks'))
        else:
            if(attempt):
                form = TaskAttemptForm(id=attempt.id, user_id=attempt.user_id, comments=attempt.comments,
                task_id= attempt.task_id, grade=attempt.grade)
            else:
                form = TaskAttemptForm(user_id=current_user.id, task_id= task.id)
    else:
        return redirect(url_for('module003.module003_tasks'))
    
    return render_template("module003_attempt_detail.html", module='module003', form=form, task_name=task.name,
        attachment_id=attempt.attachment if attempt else None)
