import os
from flask import Flask,render_template,flash,url_for,redirect,Blueprint,abort,send_from_directory,current_app
from . import db
from .models import Upldoc,User

publicprofile = Blueprint('publicprofile',__name__)

@publicprofile.route('/public/profile/<int:userid>',methods=['GET'])
def show_public_profile(userid):
    if userid:
        userdata =User.query.filter_by(id=int(userid)).first()
        if userdata:
            docdata = Upldoc.query.filter_by(userid= int(userid),private=False).all()
            return render_template('publicprofile.html',mytitle=userdata.username,user=userdata,upldocs=docdata)
        else:
            abort(404)
    else:
        abort(404)

@publicprofile.route('/public/show/doc/<string:filetoshow>')
def public_show_doc(filetoshow):
    return send_from_directory(current_app.config['USER_DOCS_UPLOAD_DIR'],str(filetoshow),as_attachment=False)

@publicprofile.route('/public/download/doc/<string:filetodown>')
def public_download_doc(filetodown):
    return send_from_directory(current_app.config['USER_DOCS_UPLOAD_DIR'],str(filetodown),as_attachment=True)

@publicprofile.route('/public/show/avatar/<string:avatar>',methods=['GET'])
def public_show_avatar(avatar):#show the avatar fetch form database
    return send_from_directory(current_app.config['USER_AVATAR_UPLOAD_DIR'],str(avatar))