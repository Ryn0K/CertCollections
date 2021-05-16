from flask import Blueprint,render_template,request,flash,redirect,url_for,abort
from . import db
from .models import User,Reportissue
from flask_wtf.csrf import CSRFError
from werkzeug.utils import escape

report = Blueprint('report',__name__)
@report.route('/report')
def issuereport():
    return render_template('report.html',mytitle = 'Report')
@report.route('/report',methods=['POST'])
def issuereport_post():
    email = escape(request.form.get('email'))
    name = escape(request.form.get('name'))
    issue = escape(request.form.get('issue'))
    if email and name and issue:
        new_report = Reportissue(name=name,email=email,issue=issue)
        db.session.add(new_report)
        db.session.commit()
        flash('Issue successfully submitted,we will contact you soon','green')
        return redirect(url_for('report.issuereport'))
    else:
        flash('Something went wrong.','red')    
        return redirect(url_for('report.issuereport'))
@report.errorhandler(CSRFError)
def handle_csrf_error(e):
    return abort(400)