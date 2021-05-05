from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, DateTimeField, SelectField, HiddenField, TextAreaField, SubmitField, FileField #, DateField
from wtforms.validators import InputRequired, Length, Optional
from wtforms.fields.html5 import DateField, TimeField, DateTimeLocalField, DecimalRangeField
import datetime


class TaskForm(FlaskForm): # class RegisterForm extends FlaskForm
    id = StringField('id')
    name = StringField('Task Name',validators=[InputRequired(),Length(min=1,max=50)])
    description = TextAreaField('Task Description',validators=[InputRequired(),Length(min=1,max=4000)])
    course_id = SelectField('Course', choices = [], validators = [InputRequired()])
    date_limit = DateTimeLocalField('Choose an expiring date',format='%Y-%m-%d %H:%M', default=datetime.datetime.today)

class TaskAttemptFilterForm(FlaskForm): # class RegisterForm extends FlaskForm
    task = SelectField('Task', choices = [(-1, "Todas las tareas")], validators = [InputRequired()], default=-1)
    submit = SubmitField('Filtrar')


class TaskAttemptForm(FlaskForm): # class RegisterForm extends FlaskForm
    id = StringField('id')
    task_id = StringField('task_id')
    user_id = StringField('user_id')
    comments = TextAreaField('Comments')
    attachment = FileField('Attachment', validators=[Optional()])
    grade = DecimalRangeField('Grade', min=0, max=10)
