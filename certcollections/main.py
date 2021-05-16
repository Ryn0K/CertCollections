from flask import Blueprint,render_template,redirect,url_for
from flask_login import login_required,current_user
from . import db
from .models import User,Upldoc
from flask_login import login_user,logout_user,login_required,current_user

main = Blueprint('main',__name__)

@main.route('/')
def index():
	if current_user.is_authenticated and (not current_user.admin):
		data = Upldoc.query.filter_by(userid=int(current_user.id)).all()
		return render_template('index.html',mytitle="Dashboard",upldocs=data)
	if current_user.admin: # if current user is admin
		return redirect(url_for('admin.index'))
	return render_template('index.html',mytitle='Home')

