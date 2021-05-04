from flask_admin import Admin, AdminIndexView
from flask_login import current_user
from wtforms import PasswordField
from flask_admin.contrib.sqla import ModelView
from werkzeug.security import generate_password_hash
from flask_admin.menu import MenuLink
from models import User, Course, Follow, ParticipationCode, ParticipationRedeem, get_db
db = get_db()

class AdminView(AdminIndexView):
    def is_accessible(self):
        if current_user.is_authenticated and current_user.profile in ('admin'):
            return True
        else:
            return False

class ProtectedView(ModelView):
    def is_accessible(self):
        if current_user.is_authenticated and current_user.profile in ('admin'):
            return True
        else:
            return False

class UserAdmin(ProtectedView):
    column_exclude_list = ('password')
    form_excluded_columns = ('password')
    column_auto_select_related = True
    def scaffold_form(self):
        form_class = super(UserAdmin, self).scaffold_form()
        form_class.password2 = PasswordField('New Password')
        return form_class
    def on_model_change(self, form, model, is_created):
        if len(model.password2):
            model.password = generate_password_hash(model.password2,method='sha256')
    def is_accessible(self):
        return current_user.is_authenticated and current_user.profile in ('admin')




admin = None

def init_admin(app):
    global admin
    if admin == None:
        admin = Admin(template_mode="bootstrap3",index_view=AdminView())
        admin.init_app(app)
        admin.add_view(UserAdmin(User,db.session))
        admin.add_view(ProtectedView(Course,db.session))
        admin.add_view(ProtectedView(Follow,db.session))
        admin.add_view(ProtectedView(ParticipationCode,db.session))
        admin.add_view(ProtectedView(ParticipationRedeem,db.session))
        admin.add_link(MenuLink(name="Logout", url="/logout"))
        admin.add_link(MenuLink(name="Go back", url="/"))
    return admin


