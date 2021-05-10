from flask import Blueprint, render_template, abort, flash, redirect, url_for, request

from flask_login import login_required, current_user
from sqlalchemy import or_, and_
from models import get_db, User, Course, Follow, ParticipationCode, ParticipationRedeem

#from models import Post, Permission, init_db, User
#from .decorators import permission_required
#from .errors import forbidden
from .forms import *


module002 = Blueprint("module002", __name__,static_folder="static",template_folder="templates")

@module002.route('/')
@login_required
def module002_index():
    #user = User.filter_by(id=current_user.id)
    if current_user.profile in ('admin','staff','student'):

        form = PostForm()
        """
        if current_user.can(Permission.WRITE) and form.validate_on_submit():
            post = Post(body=form.body.data,
                        author=current_user._get_current_object())
            db.session.add(post)
            db.session.commit()
            return redirect(url_for('.index'))
        """
        page = request.args.get('page', 1, type=int)
        show_followed = False
        if current_user.is_authenticated:
            show_followed = bool(request.cookies.get('show_followed', ''))

        #if show_followed:
            #query = current_user.followed_posts
        #else:
         #   query = Post.query
        #pagination = query.order_by(Post.timestamp.desc()).paginate(
         #   page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
          #  error_out=False)
        #posts = pagination.items
        posts = ["asda", "asdad"]
        """
        return render_template('index.html', form=form, posts=posts,
                               show_followed=show_followed, pagination=pagination)
    """
        return render_template('module002_index.html', form=form, posts=posts,
                           show_followed=show_followed)
    else:
        flash("Access denied!")
#        abort(404,description="Access denied!")
        return redirect(url_for('index'))

"""
@module002.route('/posts/')
@login_required
def get_posts():
    page = request.args.get('page', 1, type=int)
    pagination = Post.query.paginate(
        page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
        error_out=False)
    posts = pagination.items
    prev = None
    if pagination.has_prev:
        prev = url_for('api.get_posts', page=page-1)
    next = None
    if pagination.has_next:
        next = url_for('api.get_posts', page=page+1)
    return jsonify({
        'posts': [post.to_json() for post in posts],
        'prev': prev,
        'next': next,
        'count': pagination.total
    })


@module002.route('/posts/<int:id>')
@login_required
def get_post(id):
    post = Post.query.get_or_404(id)
    return jsonify(post.to_json())


@module002.route('/posts/', methods=['POST'])
@login_required
#@permission_required(Permission.WRITE)
def new_post():
    post = Post.from_json(request.json)
    post.author = g.current_user
    init_db.session.add(post)
    init_db.session.commit()
    return jsonify(post.to_json()), 201, \
        {'Location': url_for('api.get_post', id=post.id)}


@module002.route('/posts/<int:id>', methods=['PUT'])
@login_required
#@permission_required(Permission.WRITE)
def edit_post(id):
    post = Post.query.get_or_404(id)
    if g.current_user != post.author and \
            not g.current_user.can(Permission.ADMIN):
        return flash('Insufficient permissions')
    post.body = request.json.get('body', post.body)
    init_db.session.add(post)
    init_db.session.commit()
    return jsonify(post.to_json())

"""




@module002.route('/test')
def module002_test():
    return 'OK'
