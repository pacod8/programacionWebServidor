from flask import Flask

app = None

def init_app(name):
    global app
    if app == None:
        app = Flask(name)
    return app

def get_app():
    global app
    if app == None:
        app = init_app(__name__)
    return app

