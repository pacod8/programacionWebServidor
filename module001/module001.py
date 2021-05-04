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
                try:
                    db.session.commit()
                    flash("Course created successfully with code: {}".format(course.code))
                except:
                    db.session.rollback()
                    flash("Error creating course!")
            else:
                change = 0
                course = Course.query.get(form.id.data)
                newcoursename = form.name.data.strip().replace('-' + course.code,'') + '-' + course.code
                if course.name != newcoursename:
                    course.name = newcoursename
                    change = 1

                newinstitutionname = form.institution_name.data.strip()
                if course.institution_name != newinstitutionname:
                    course.institution_name = newinstitutionname
                    change = 1

                try:
                    if change:
                        db.session.commit()
                        flash("Course  updated successfully!")
                    else:
                        flash("Nothing has changed!")
                except:
                    db.session.rollback()
                    flash("Error updating course!")
                return redirect(url_for('module001.module001_course'))

    elif ('rowid' in request.args):
        course = Course.query.get(request.args['rowid'])
        if not course or course.user_id != current_user.id:
            flash('Error retrieving data for the course {}'.format(request.args['rowid']))
        else:
            form = CourseForm(id=course.id, name=course.name.replace('-' + course.code,''), institution_name = course.institution_name, code=course.code)

    courses = Course.query.filter_by(user_id=current_user.id)
    return render_template("module001_course.html",module="module001", form=form, rows=courses)


from qrcode import QRCode, ERROR_CORRECT_L
@module001.route('/sharing_details',methods=['GET','POST'])
@login_required
def sharing_details():
    qr = QRCode(version=20, error_correction=ERROR_CORRECT_L)

    if request.args.get('itemtype') == 'course':
        course = Course.query.get(request.args.get('rowid'))
        if not course or course.user_id != current_user.id:
            flash("An error has occurred retrieving details for the activity")
            return redirect(url_for('library'))
        qr.add_data("http://attendance.pythonanywhere.com/follow?sharedlink=1&code={}".format(course.code))
        module,itemtype,item="library","course",course
#    else:
#        participation = ParticipationCode.query.get(request.args.get('rowid'))
#        if not participation or participation.user_id != current_user.id:
#            flash("An error has occurred retrieving details for the participation")
#            return redirect(url_for('participation_generate'))
#        qr.add_data("http://attendance.pythonanywhere.com/participation_redeem?sharedlink=1&code={}".format(participation.code))
#        module,itemtype,item="participation_gerenate","participation",participation
    try:
        qr.make() # Generate the QRCode itself
        im = qr.make_image()
        filename = "./static/qrcodes/{}.png".format(item.code)
        im.save(filename)
        return render_template('module001_sharing_details.html',module=module, item=item, itemtype=itemtype,filename=filename,baseurl=request.host)
    except:
        return render_template('module001_sharing_details.html',module=module, item=item, itemtype=itemtype,base_url=request.host)



@module001.route('/test')
def module001_test():
    return 'OK'





















