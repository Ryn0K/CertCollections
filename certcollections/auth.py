from flask import render_template,redirect,url_for,request,flash,Blueprint,Markup,abort
from werkzeug.security import generate_password_hash,check_password_hash
from werkzeug.utils import escape
from . import db
from .models import User
from flask_login import login_user,logout_user,login_required,current_user
from flask_admin import Admin
from flask_wtf.csrf import CSRFError
from flask_admin.contrib.sqla import ModelView
auth = Blueprint('auth',__name__)

@auth.route('/login')
def login():
	if current_user.is_authenticated:
		if current_user.admin:
			return redirect(url_for('admin.index'))
		return redirect(url_for('main.index'))
	return render_template('login.html',mytitle='Login')

@auth.route('/login',methods=['POST'])
def login_post():
	if current_user.is_authenticated:
		if current_user.admin:
			return redirect(url_for('admin.index'))
		return redirect(url_for('main.index'))
	email = escape(request.form.get('email'))
	passw = escape(request.form.get('password'))
	if email and passw:
		user = User.query.filter_by(email = email).first()
		if(not user) or (not check_password_hash(user.password,passw)):
			flash('Invalid email or password','red')
			return redirect(url_for('auth.login'))
		else:
			login_user(user,remember=True) # login the user
			return redirect(url_for('main.index'))
	else:
		flash('Must provide email and password to login','red')
		return redirect(url_for('auth.login'))
@auth.route('/register')
def register():
	return render_template('register.html',mytitle='Register')

@auth.route('/register',methods=['POST'])
def register_post():
	email = escape(request.form.get('email'))
	username = escape(request.form.get('username'))
	password = escape(request.form.get('password'))
	Cpassword = escape(request.form.get('Cpassword'))
	if email and username and password and Cpassword and (password == Cpassword):
		user = User.query.filter_by(email=email).first()
		if user:# account already exist
			flash(Markup('Email already exist.<a href="/login">login here....</a>'),'orange')
			return redirect(url_for('auth.register'))
		else:
			new_user = User(email = email,username = username , password = generate_password_hash(password,method='sha256'))
			db.session.add(new_user)
			db.session.commit()
			flash(u'Account created successfully,now login','green')
			return redirect(url_for('auth.login'))
	else:
		flash(u'Error while creating account,Must provide all details.','red')
		return redirect(url_for('auth.register'))

@auth.route('/logout')
@login_required
def logout():
	logout_user()
	return redirect(url_for('main.index'))