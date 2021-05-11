from flask import Blueprint, render_template, abort, flash, redirect, url_for, request
from flask_login import login_required, current_user
from sqlalchemy import or_, and_
from models import get_db, User, Course, Follow, ParticipationCode, ParticipationRedeem
import random
import datetime

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
def module001_sharing_details():
    qr = QRCode(version=20, error_correction=ERROR_CORRECT_L)
    base_url=request.host
    if request.args.get('itemtype') == 'course':
        course = Course.query.get(request.args.get('rowid'))
        if not course or course.user_id != current_user.id:
            flash("An error has occurred retrieving details for the activity")
            return redirect(url_for('module001.module001_course'))
        qr.add_data("http://{}/course/follow?sharedlink=1&code={}".format(base_url,course.code))
        module,itemtype,item="library","course",course
    else:
        participation = ParticipationCode.query.get(request.args.get('rowid'))
        if not participation or participation.user_id != current_user.id:
            flash("An error has occurred retrieving details for the participation")
            return redirect(url_for('module001.module001_participation_generate'))
        qr.add_data("http://{}/course/participation_redeem?sharedlink=1&code={}".format(base_url,participation.code))
        module,itemtype,item="participation_gerenate","participation",participation
    try:
        qr.make() # Generate the QRCode itself
        im = qr.make_image()
        filename = "./static/qrcodes/{}.png".format(item.code)
        urlfilename = "http://{}/static/qrcodes/{}.png".format(base_url,item.code)
        im.save(filename)
        return render_template('module001_sharing_details.html',module="module001", item=item, itemtype=itemtype,filename=urlfilename,base_url=base_url)
    except:
        return render_template('module001_sharing_details.html',module="module001", item=item, itemtype=itemtype,base_url=base_url)


@module001.route('/follow',methods=['GET','POST'])
@login_required
def module001_follow():
    form = FollowForm()
    unfollow=False
    if request.method == 'POST':
        if form.validate_on_submit():
            course_code = form.code.data
            follow = Follow.query.filter(and_(Follow.course_code==form.code.data,
                                              Follow.user_id==current_user.id)).first()
            if follow:
                flash("You are already following the course {} ".format(course_code))
            else:
                course = Course.query.filter_by(code=form.code.data).first()
                if not course:
                    flash('The code {} is invalid, try again with the correct code.'.format(form.code.data))
                else:
                    follow = Follow(user_id=current_user.id,
                                    course_id=course.id,
                                    course_code=course.code,
                                    course_name=course.name,
                                    institution_name = course.institution_name)
                    try:
                        db.session.add(follow)
                        db.session.commit()
                        flash("You are now following {}".format(course.name))
                    except:
                        db.session.rollback()
                        flash("Error following!")
    elif ('sharedlink' in request.args):
        form=FollowForm(code=request.args.get('code'))

    follows = Follow.query.filter_by(user_id=current_user.id)
    return render_template('module001_follow.html',module="module001", form=form, rows=follows, unfollow=unfollow)

@module001.route('/unfollow',methods=['GET','POST'])
@login_required
def module001_unfollow():
    form = FollowForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            course_code = form.code.data
            follow = Follow.query.filter(and_(Follow.course_code==form.code.data,
                                              Follow.user_id==current_user.id)).first()
            if follow:
                try:
                    db.session.delete(follow)
                    db.session.commit()
                    flash("You are not following {} any longer".format(course_code))
                    return redirect(url_for('module001.module001_follow'))
                except:
                    db.session.rollback()
                    flash("Error unfollowing!")
        flash('Something unusual happened, please try again later')
    else:
        form=FollowForm(code=request.args.get('code'))
    unfollow=True
    follows = Follow.query.filter_by(user_id=current_user.id)

    return render_template('module001_follow.html',module="module001", form=form, rows=follows, unfollow=unfollow)


@module001.route('/participation_generate',methods=['GET','POST'])
@login_required
def module001_participation_generate():
    form = ParticipationCodeForm()
    if request.method == 'POST':
        try:
            if not form.id.data:
                course = Course.query.get(form.course_id.data)
                while(True):
                    participation_code = 'P'+str(form.course_id.data)+''.join(random.choice('AILNOQVBCDEFGHJKMPRSTUXZ') for i in range(4))
                    participation = ParticipationCode.query.filter_by(code=participation_code).first()
                    if not participation:
                        break
                if course:
                    if form.never_expire.data:
                        participation = ParticipationCode(
                                code = participation_code,
                                code_description =  form.code_description.data,
                                code_type = form.code_type.data,
                                user_id = current_user.id,
                                course_id = course.id,
                                course_name = course.name,
                                institution_name = course.institution_name)
                    else:
                        participation = ParticipationCode(
                                code = participation_code,
                                code_description =  form.code_description.data,
                                code_type = form.code_type.data,
                                user_id = current_user.id,
                                course_id = course.id,
                                course_name = course.name,
                                institution_name = course.institution_name,
                                date_expire=datetime.datetime.combine(form.date_expire.data, form.time_expire.data))
                    db.session.add(participation)
                    db.session.commit()
                    flash("Participation code {} created successfully".format(participation.code))
                else:
                    flash("Error selecting course")
                return redirect(url_for('module001.module001_participation_generate'))
            else:
#                flash("date_expire={} / time_expire={}".format(type(form.date_expire.data),type(form.time_expire.data)))
#                flash("Date time combined={}".format(datetime.datetime.combine(form.date_expire.data, form.time_expire.data)))
#                return redirect(url_for('module001.module001_participation_generate'))
                course = Course.query.get(int(form.course_id.data))
                participation = ParticipationCode.query.get(form.id.data)

                newname = form.code_description.data.strip()
                if course.institution_name != newname:
                    oldname = participation.code_description
                    db.session.query(ParticipationRedeem).filter(ParticipationRedeem.code_description==oldname).update({ParticipationRedeem.code_description:newname}, synchronize_session=False)

                if course:
                    participation.code_description =  form.code_description.data
                    participation.code_type = form.code_type.data
                    participation.course_id = form.course_id.data
                    participation.course_name = course.name
                    participation.institution_name = course.institution_name
                    if form.never_expire.data:
                        participation.date_expire=None
                    else:
                        participation.date_expire=datetime.datetime.combine(form.date_expire.data, form.time_expire.data)
                else:
                    participation.code_description =  form.code_description.data
                    participation.code_type = form.code_type.data
                    participation.user_id = current_user.id
                    participation.course_id = 0
                    participation.course_name = 'all'
                    participation.institution_name = 'all'
                    if form.never_expire.data:
                        participation.date_expire=None
                    else:
                        participation.date_expire=datetime.datetime.combine(form.date_expire.data, form.time_expire.data)
                db.session.commit()
                flash("Participation code {} updated successfully".format(participation.code))
                return redirect(url_for('module001.module001_participation_generate'))
        except:
            db.session.rollback()
            flash("Error creating / updating participation!")


#    elif ('redeems' in request.args) and ('rowid' in request.args):
#        participation = ParticipationCode.query.get(request.args.get('rowid'))
#        participations = ParticipationRedeem.query.filter(ParticipationRedeem.participation_code == participation.code)
#        rows = [(User.query.filter_by(id=item.user_id).first(), item.date_created, item.date_modified) for item in participations]
#        return render_template('participation_redeem_dashboad.html',module="participation_generate", form=form, rows=rows, participation_code=participation.code)
    elif ('coursename' in request.args) and ('rowid' in request.args):
        form = ParticipationCodeForm(course_id=request.args.get('rowid'))
    elif ('rowid' in request.args):
        participation = ParticipationCode.query.get(request.args.get('rowid'))
        form = ParticipationCodeForm(id=participation.id,
                                     code_description = participation.code_description,
                                     code=participation.code,
                                     course_id=participation.course_id,
                                     code_type=participation.code_type,
                                     never_expire=(participation.date_expire == None),
                                     date_expire=participation.date_expire,
                                     time_expire=participation.date_expire)
    else:
        form = ParticipationCodeForm(course_id=0)


    participations = ParticipationCode.query.filter(ParticipationCode.user_id==current_user.id)

    for course in Course.query.filter_by(user_id=current_user.id):
        form.course_id.choices += [(course.id,  str(course.id) + ' - ' + course.institution_name + ' - ' + course.name)]
    return render_template('module001_participation_generate.html',module="module001", form=form, rows=participations)

@module001.route('/participation_redeem',methods=['GET','POST'])
@login_required
def module001_participation_redeem():
    form = ParticipationRedeemForm()
    unfollow=False
    if request.method == 'POST':
        if form.validate_on_submit():
            code = form.code.data.strip()
            participation = ParticipationCode.query.filter_by(code=code).first()
            if not participation:
                flash('Invalid code')
                return redirect(url_for('module001.module001_participation_redeem'))

            redeem = ParticipationRedeem.query.filter(ParticipationRedeem.participation_code == code,
                                             ParticipationRedeem.user_id == current_user.id).first()
            if redeem:
                flash("You have already redeemed this code")
                return redirect(url_for('module001.module001_participation_redeem'))
            participation = ParticipationCode.query.filter(ParticipationCode.code==code,
                                                           or_(ParticipationCode.date_expire == None,
                                                               ParticipationCode.date_expire > datetime.datetime.now())).first()
            if not participation:
                flash('Participation code is expired')
                return redirect(url_for('module001.module001_participation_redeem'))

            follow = Follow.query.filter(Follow.course_id==participation.course_id,
                                         Follow.user_id==current_user.id).first()
            if not follow:
                flash('You are not following this course. Ask the course code for the professor and follow the course before redeeming any participation.')
            else:
                course = Course.query.get(participation.course_id)
                redeem = ParticipationRedeem(
                        participation_code = participation.code,
                        code_description = participation.code_description,
                        user_id = current_user.id,
                        course_id = course.id,
                        course_name = course.name,
                        institution_name = course.institution_name)
                db.session.add(redeem)
                db.session.commit()
                flash("Participation code {} redeemed successfully".format(participation.code))
                return redirect(url_for('module001.module001_participation_redeem'))
    elif ('sharedlink' in request.args):
        form=FollowForm(code=request.args.get('code'))
    elif ('rowid' in request.args):
        participation = ParticipationRedeem.query.get(request.args.get('rowid'))
        if participation:
            if participation.user_id != current_user.id:
                flash("User not authorised for this content")
            else:
                form = ParticipationRedeemForm(code=participation.participation_code)
        unfollow=True
    participations = ParticipationRedeem.query.filter(ParticipationRedeem.user_id==current_user.id)
    return render_template('module001_participation_redeem.html',module="participation_redeem", form=form, rows=participations,unfollow=unfollow)

@module001.route('/participation_redeem_delete',methods=['POST','GET'])
@login_required
def module001_participation_redeem_delete():
    form = ParticipationRedeemForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            code = form.code.data.strip()
            redeem = ParticipationRedeem.query.filter(ParticipationRedeem.participation_code == code,
                                             ParticipationRedeem.user_id == current_user.id).first()
            if redeem:
                participation_code = redeem.participation_code
                db.session.delete(redeem)
                db.session.commit()
                flash("Code {} has been removed, you can always redeem again if you are still within the deadline".format(participation_code))
                return redirect(url_for('module001.module001_participation_redeem'))
    else:
        redeem = ParticipationRedeem.query.filter(ParticipationRedeem.participation_code == request.args.get('participation_code'),
                                         ParticipationRedeem.user_id == request.args.get('used_id')).first()
        if redeem:
            participation_code = redeem.participation_code
            db.session.delete(redeem)
            db.session.commit()
            flash("Code {} has been removed from user {}, user can always redeem again if still within the deadline (extending the deadlines works)".format(participation_code,request.args.get('used_id')))
            return redirect(url_for('module001.module001_participation_generate'))

    flash('Something unusual happened, please try again later')
    return redirect(url_for('module001.module001_participation_redeem'))



@module001.route('/test')
def module001_test():
    return 'OK'





















