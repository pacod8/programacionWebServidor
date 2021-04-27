from flask import Blueprint, render_template, abort, flash, redirect, url_for
from flask_login import login_required, current_user
from models import get_db, User
module001 = Blueprint("module001", __name__,static_folder="static",template_folder="templates")
db = get_db()


@module001.route('/')
@login_required
def module001_index():
    user = User.query.filter_by(id=current_user.id).first()
    if current_user.profile in ('admin','staff','student'):
        return render_template("module001_index.html",module="module001", user=user)
    else:
        flash("Access denied!")
#        abort(404,description="Access denied!")
        return redirect(url_for('index'))

@module001.route('/test')
def module001_test():
    return 'OK'