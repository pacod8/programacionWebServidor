from flask import Blueprint, render_template, abort, flash, redirect, url_for
from flask_login import login_required, current_user

module002 = Blueprint("module002", __name__,static_folder="static",template_folder="templates")

@module002.route('/')
@login_required
def module002_index():
    #user = User.filter_by(id=current_user.id)
    if current_user.profile in ('admin','staff','student'):
        return render_template("module002_index.html",module="module002")
    else:
        flash("Access denied!")
#        abort(404,description="Access denied!")
        return redirect(url_for('index'))


@module002.route('/test')
def module002_test():
    return 'OK'
