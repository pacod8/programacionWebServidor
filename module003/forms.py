import datetime
from decimal import *

from flask_wtf import FlaskForm
from flask_wtf.file import FileField
from wtforms import StringField, BooleanField, DateTimeField, SelectField, HiddenField, TextAreaField, SubmitField #, DateField
from wtforms.validators import InputRequired, Length, Optional, ValidationError
from wtforms.fields.html5 import DateField, TimeField, DateTimeLocalField, DecimalField


class TaskForm(FlaskForm): # class RegisterForm extends FlaskForm
    id = StringField('id')
    name = StringField('Task Name',validators=[InputRequired(),Length(min=1,max=50)])
    description = TextAreaField('Task Description',validators=[InputRequired(),Length(min=1,max=4000)])
    course_id = SelectField('Course', choices = [], validators = [InputRequired()])
    date_limit = DateTimeLocalField('Choose an expiring date',format='%Y-%m-%d %H:%M', default=datetime.datetime.today)

class TaskAttemptFilterForm(FlaskForm): # class RegisterForm extends FlaskForm
    task = SelectField('Task', choices = [(-1, "Todas las tareas")], validators = [InputRequired()], default=-1)
    submit = SubmitField('Filtrar')

def grades_validator():
    message = 'Must be between 0 and 10.'

    def _validator(form, field):
        l = field.data
        if l != None:
            if not type(l) in [float, int, Decimal] or l < 0 or l > 10 :
                raise ValidationError(message)

    return _validator

class TaskAttemptForm(FlaskForm): # class RegisterForm extends FlaskForm
    id = StringField('id')
    task_id = StringField('task_id')
    user_id = StringField('user_id')
    comments = TextAreaField('Comments')
    attachment = FileField('Attachment')
    grade = DecimalField('Grade', validators=[Optional(), grades_validator()])
