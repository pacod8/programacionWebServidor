from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import InputRequired, Length

class CourseForm(FlaskForm): # class RegisterForm extends FlaskForm
    id = StringField('id')
    name = StringField('Course Name',validators=[InputRequired(),Length(min=1,max=50)])
    institution_name = StringField('Institution Name')
    code = StringField('Course Code')
