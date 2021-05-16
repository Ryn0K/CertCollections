from flask import redirect,url_for,Markup,flash,abort
from flask_admin import Admin,AdminIndexView,expose,helpers
from flask_admin.contrib.sqla import ModelView
from . import db
from .models import User,Reportissue,Upldoc
from flask_login import current_user


class MyModelView(ModelView):
	'''this is just a child class of ModelView with some modifications'''
	def is_accessible(self):
		return current_user.admin

class MyAdminIndexView(AdminIndexView):
	@expose('/')
	def index(self):
		if (current_user.is_authenticated) and (not current_user.admin):
			abort(403) # send not authorised
		if not current_user.admin:
			flash(Markup('Please login as <b>Admin</b> first.'),'red')
			return redirect(url_for('auth.login'))
		return super(MyAdminIndexView,self).index()
class SetFlaskAdmin():
	def __init__(self,app):
		self.admin = Admin(app,name='CertCollections',index_view=MyAdminIndexView(),base_template='admin_template.html')
		self.admin.add_view(MyModelView(User,db.session))
		self.admin.add_view(MyModelView(Reportissue,db.session))
		self.admin.add_view(MyModelView(Upldoc,db.session))	