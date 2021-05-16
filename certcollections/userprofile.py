from flask import Blueprint,render_template,flash,redirect,url_for,request,abort
from flask_login import current_user,login_required,logout_user
from werkzeug.security import generate_password_hash,check_password_hash
from werkzeug.utils import escape
from . import db
from .models import User
from flask_wtf.csrf import CSRFError
userprofile = Blueprint('userprofile',__name__)


@userprofile.route('/user/edit')
@login_required
def useredit():
	return render_template('user_edit.html',mytitle = 'Edit Profile')

@userprofile.route('/user/edit',methods=['POST'])
@login_required
def useredit_post():
	id_user = current_user.id
	if (id_user == 0): # anonymous user
		abort(403)
	entry = User.query.filter_by(id = id_user).first()
	# first check for password
	oldpassword = escape(request.form.get('oldpassword'))
	if oldpassword:
		if not check_password_hash(entry.password,oldpassword):
			#password match fail
			flash('Invalid old password.','red')
			return redirect(url_for('userprofile.useredit'))
		entry.username = escape(request.form.get('username')) if escape((request.form.get('username')) != entry.username) else entry.username
		if((request.form.get('email') != entry.email) and User.query.filter_by(email = request.form.get('email')).first()):
			#email should be unique ,checking if already exists.
			flash('Email already exists','orange')
			return redirect(url_for('userprofile.useredit'))
		entry.email = escape(request.form.get('email')) if (escape(request.form.get('email')) != entry.email) else entry.email	
		newpass = escape(request.form.get('newpassword'))
		cnewpass = escape(request.form.get('Cnewpassword'))
		# if newpass and cnewpass is given by the user
		if newpass and cnewpass:
			if (len(newpass) > 6) and (len(cnewpass) > 6) and (newpass == cnewpass):
				newpasshash = generate_password_hash(newpass,method='sha256')
				entry.password =  newpasshash if (newpasshash != entry.password) else entry.password
			else:
				flash('Newpassword must be atleast 6 character long and equal to confirm password','red')
				return redirect(url_for('userprofile.useredit'))
		db.session.commit()# commit changes
		flash('Profile updated successfully.','green')
		return redirect(url_for('userprofile.useredit'))
	else:
		flash('Something wrong happening','orange')
		return redirect(url_for('userprofile.useredit'))


@userprofile.route('/user/delete/<int:userid>')
@login_required
def deleteuser(userid):
	if userid == current_user.id and userid != 0: # confirm with session and should not anonymous user
		User.query.filter_by(id = userid).delete()
		db.session.commit()
		logout_user()
		return redirect(url_for('main.index',showmessage='Your account deleted successfully.'))
	else:
		abort(403)