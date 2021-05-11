from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, DateTimeField, SelectField, HiddenField#, DateField
from wtforms.validators import InputRequired, Length
from wtforms.fields.html5 import DateField, TimeField, DateTimeLocalField
import datetime


class CourseForm(FlaskForm): # class RegisterForm extends FlaskForm
    id = StringField('id')
    name = StringField('Course Name',validators=[InputRequired(),Length(min=1,max=50)])
    institution_name = StringField('Institution Name')
    code = StringField('Course Code')

class FollowForm(FlaskForm): # class RegisterForm extends FlaskForm
    code = StringField('Enter the course code you wish to follow / unfollow:',validators=[InputRequired(),Length(min=1,max=50)])


class ParticipationCodeForm(FlaskForm): # class RegisterForm extends FlaskForm
    id = StringField('id')
    code = StringField('Participation/Bonus Code')
    code_description = StringField('Participation/Bonus Description (ex: forum 30/march/2021)',validators=[Length(max=50)])
    code_type = SelectField('Type', choices = [('public','public'),('private','private'),('non-redeemable','non-redeemable')], validators = [InputRequired()])
    course_id = SelectField('Course (must create a library first)', choices = [], validators = [InputRequired()])
    never_expire = BooleanField('Never expire')
    date_expire = DateField('Choose an expiring date',format='%Y-%m-%d', default=datetime.datetime.today)
    time_expire = TimeField('Expiring time',format='%H:%M', default=datetime.time(23, 59))

class ParticipationRedeemForm(FlaskForm): # class RegisterForm extends FlaskForm
    code = StringField('Enter the code you wish to redeem', validators = [InputRequired()])
