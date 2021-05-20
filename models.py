from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

import datetime

db = None

def init_db(app):
    global db
    if db == None:
        db = SQLAlchemy(app) # class db extends app
    return db

def get_db():
    global db
    if db == None:
        from application import get_app
        app = get_app()
        db = init_db(app)
    return db

from application import get_app
app = get_app()
db = init_db(app)

class User(UserMixin,db.Model): # User extends db.Model
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50),unique=True)
    username = db.Column(db.String(15),unique=True)
    password = db.Column(db.String(80))
    profile = db.Column(db.String(10),default='student') # 'admin', 'staff', 'professor', 'student'
    confirmed = db.Column(db.Boolean(),default=False)
    userhash = db.Column(db.String(50))

    date_created  = db.Column(db.DateTime,  default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime,  default=db.func.current_timestamp(),
                                       onupdate=db.func.current_timestamp())
    course = db.relationship('Course', backref='user', lazy=True)

    ######
    #posts = db.relationship('Post', backref='author', lazy='dynamic')


class Course(UserMixin,db.Model): # User extends db.Model
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    institution_name = db.Column(db.String(50))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    code = db.Column(db.String(50),unique=True)

    date_created  = db.Column(db.DateTime,  default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime,  default=db.func.current_timestamp(),
                                       onupdate=db.func.current_timestamp())
    follow = db.relationship('Follow', backref='course', lazy=True)

class Follow(UserMixin,db.Model): # User extends db.Model
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)
    course_name = db.Column(db.String(50))
    course_code = db.Column(db.String(50))
    institution_name = db.Column(db.String(50))

    date_created  = db.Column(db.DateTime,  default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime,  default=db.func.current_timestamp(),
                                       onupdate=db.func.current_timestamp())


class ParticipationCode(UserMixin,db.Model): # User extends db.Model
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(50))
    code_description = db.Column(db.String(120))
    code_type = db.Column(db.String(50))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)
    course_name = db.Column(db.String(50))
    institution_name = db.Column(db.String(50))
    date_expire = db.Column(db.DateTime)

    date_created  = db.Column(db.DateTime,  default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime,  default=db.func.current_timestamp(),
                                       onupdate=db.func.current_timestamp())

class ParticipationRedeem(UserMixin,db.Model): # User extends db.Model
    id = db.Column(db.Integer, primary_key=True)
    participation_code = db.Column(db.String(50))
    code_description = db.Column(db.String(120))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)
    course_name = db.Column(db.String(50))
    institution_name = db.Column(db.String(50))

    date_created  = db.Column(db.DateTime,  default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime,  default=db.func.current_timestamp(),
                                       onupdate=db.func.current_timestamp())

class CourseTasks(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)
    name = db.Column(db.String(50))
    description = db.Column(db.String(4000))
    date_limit  = db.Column(db.DateTime, nullable=False)

    date_created  = db.Column(db.DateTime,  default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime,  default=db.func.current_timestamp(),
                                       onupdate=db.func.current_timestamp())

class CourseTaskAttemps(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task_id = db.Column(db.Integer, db.ForeignKey('course_tasks.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    comments = db.Column(db.String(4000))
    attachment = db.Column(db.Integer, db.ForeignKey('user_file.id'))
    grade = db.Column(db.Float)
    date_created  = db.Column(db.DateTime,  default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime,  default=db.func.current_timestamp(),
                                       onupdate=db.func.current_timestamp())

class UserFile(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    filetype = db.Column(db.String(50))
    filename = db.Column(db.String(50))



class PostComments (UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    post = db.Column(db.String(4000), nullable=False)
    date_created  = db.Column(db.DateTime,  default=db.func.current_timestamp())
    course_code = db.Column(db.String(50))






