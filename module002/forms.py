from wtforms import SubmitField
from wtforms.validators import DataRequired
from flask_pagedown.fields import PageDownField
from flask_wtf import FlaskForm




class PostForm(FlaskForm):
    body = PageDownField("What's on your mind?", validators=[DataRequired()])
    submit = SubmitField('Submit')