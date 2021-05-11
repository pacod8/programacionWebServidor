from flask import Blueprint, render_template

module003 = Blueprint("module003", __name__,static_folder="static",template_folder="templates")

@module003.route('/')
def module003_index():
    return render_template("module003_index.html",module='module003')

@module003.route('/test')
def module003_test():
    return 'OK'