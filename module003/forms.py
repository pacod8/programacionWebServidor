from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, DateTimeField, SelectField, HiddenField, TextAreaField #, DateField
from wtforms.validators import InputRequired, Length
from wtforms.fields.html5 import DateField, TimeField, DateTimeLocalField
import datetime


class TaskForm(FlaskForm): # class RegisterForm extends FlaskForm
    id = StringField('id')
    name = StringField('Task Name',validators=[InputRequired(),Length(min=1,max=50)])
    description = TextAreaField('Task Description',validators=[InputRequired(),Length(min=1,max=50)])
    course_id = SelectField('Course', choices = [], validators = [InputRequired()])
    date_limit = DateTimeLocalField('Choose an expiring date',format='%Y-%m-%d %H:%M', default=datetime.datetime.today)

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