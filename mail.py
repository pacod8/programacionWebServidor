from flask_mail import Mail, Message
from flask import render_template
from application import get_app

app = get_app()

mail = None

def init_mail(app):
    global mail
    if mail == None:
        mail = Mail(app)
    return mail

def get_mail():
    return mail

def send_email(to, subject, template, url, newpassword, **kwargs):
    msg = Message(app.config['FLASKY_MAIL_SUBJECT_PREFIX'] + subject, sender=app.config['FLASKY_MAIL_SENDER'], recipients=[to])
    msg.body = render_template(template + '.txt', **kwargs, base_url=url, newpassword=newpassword)
    msg.html = render_template(template + '.html', **kwargs, base_url=url, newpassword=newpassword)
    mail.send(msg)