from flask import Blueprint, render_template, abort, flash, redirect, url_for, request, current_app
from flask_login import login_required, current_user
from sqlalchemy import or_, and_
from models import get_db, User, Course, Follow, CourseTasks, CourseTaskAttemps, UserFile
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


def get_user_courses(user):
    if user.profile == 'staff':
        courses = Course.query.filter_by(user_id=user.id).all()
    elif user.profile == 'admin':
        courses = Course.query.all()
    else:
        follows = map(lambda x: x.course_id, Follow.query.filter_by(user_id=user.id).all())
        courses = Course.query.filter(Course.id.in_(follows)).all()

    return courses, list(map(lambda x: x.id, courses))


@module003.route('/tasks', methods=['GET', 'POST'])
@login_required
def module003_tasks():
    form = TaskForm()
    courses, courses_ids = get_user_courses(current_user)
    #tasks = CourseTasks.query.filter(CourseTasks.course_id.in_(list(map(lambda x: x.id, courses))))
    for course in courses:
        form.course_id.choices += [(str(course.id),  str(course.id) + ' - ' + course.institution_name + ' - ' + course.name)]

    if request.method == 'POST' and current_user.profile != 'student':
        if form.validate_on_submit():
            if not form.id.data:
                if not int(form.course_id.data) in courses_ids:
                    flash("El curso no es de su propiedad")
                    return redirect(url_for('module003.module003_tasks'))
                task = CourseTasks(name=form.name.data.strip(),
                            description=form.description.data.strip(),
                            course_id=form.course_id.data,
                            date_limit=form.date_limit.data )
                db.session.add(task)
                db.session.commit()
                form.id.data = task.id
               
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
        course_t = Course.query.filter_by(id=task.course_id).first()
        if not task or not course_t or not task.course_id in courses_ids:
            flash('Error retrieving data for the task {}'.format(request.args['rowid']))
        else:
            form = TaskForm(id=task.id, name=task.name, description=task.description, course_id= task.course_id, date_limit=task.date_limit)
            for course in courses:
                form.course_id.choices += [(str(course.id),  str(course.id) + ' - ' + course.institution_name + ' - ' + course.name)]

    tasks = CourseTasks.query.filter(CourseTasks.course_id.in_(courses_ids)).order_by(CourseTasks.course_id).all()
    if len(courses) != 0:
        for t in tasks:
            course = list(filter(lambda x: x.id == t.course_id, courses))[0]
            t.course_name = str(course.id) + ' - ' + course.institution_name + ' - ' + course.name


    return render_template("module003_tasks.html",module="module003", form=form, rows=tasks)


@module003.route('/attempt', methods=['GET', 'POST'])
@login_required
def module003_attempt():
    filter_form = TaskAttemptFilterForm()
    courses, filter_courses = get_user_courses(current_user)
    #courses_ids = list(map(lambda x: x.id, courses))

    tasks = CourseTasks.query.filter(CourseTasks.course_id.in_(filter_courses))
    filter_task = list(map(lambda x: x.id, tasks))
    for t in tasks:
        filter_form.task.choices += [(str(t.id), t.name)]
    if(filter_form.task.data):
        filter_form.task.data = str(filter_form.task.data)

    if request.method == 'POST':
        if filter_form.validate_on_submit():
            filter_task = [filter_form.task.data] if int(filter_form.task.data) != -1 else filter_task



    attempts = CourseTaskAttemps.query.filter(CourseTaskAttemps.task_id.in_(filter_task)).all()

    for a in attempts:
        task = list(filter(lambda x: x.id == a.task_id, tasks))[0]
        print(task.name)
        a.task_name = str(task.name)
    return render_template("module003_attempt.html", module='module003', filter_form=filter_form, rows=attempts)


@module003.route('/attempt-detail', methods=['GET', 'POST'])
@login_required
def module003_attempt_detail():
    form = TaskAttemptForm()
    courses, courses_ids = get_user_courses(current_user)

    if request.method == 'POST':
        if form.validate_on_submit():
            fileatt = None
            if (form.attachment.data):
                f = form.attachment.data
                filename = f.filename.split('.')
                filename.insert(-1, str(uuid.uuid4().hex))
                filename[0] = filename[0][:10]
                filename = secure_filename('.'.join(filename))
                f.save(os.path.join(current_app.config['UPLOADS_FOLDER'], filename))
                filetype = f.mimetype

                fileatt = UserFile(filename=filename, filetype=filetype, user_id=current_user.id)
                db.session.add(fileatt)
                db.session.commit()
            if(not form.id.data):
                task = CourseTasks.query.filter_by(id=form.task_id.data).first()
                if not task or not task.course_id in courses_ids or current_user.profile != 'student':
                    flash('Error updating attempt for task {}'.format(form.task_id.data))
                    return redirect(url_for('module003.module003_attempts'))

                attempt = CourseTaskAttemps(task_id=form.task_id.data, user_id=current_user.id,
                    comments=form.comments.data, attachment=fileatt.id if fileatt else None)
            else:
                attempt = CourseTaskAttemps.query.filter_by(id=form.id.data).first()
                if current_user.profile in ['admin', 'staff']:
                    attempt.grade = form.grade.data
                else:
                    attempt.comments = form.comments.data
                    attempt.attachment = fileatt.id if fileatt else attempt.attachment
            db.session.add(attempt)
            db.session.commit()
            task = CourseTasks.query.filter_by(id=form.task_id.data).first()
            form.id.data = attempt.id
        else:
            flash('Error en el formulario')
            return redirect(url_for('module003.module003_attempt'))
    elif ('taskid' in request.args):
        attempt = CourseTaskAttemps.query.filter_by(task_id=request.args['taskid']).first()
        task = CourseTasks.query.filter_by(id=request.args['taskid']).first()
        if not task or not task.course_id in courses_ids:
            flash('Error retrieving data for the attempt {}'.format(request.args['taskid']))
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
