import os
from uuid import uuid4
from flask import Flask, render_template, flash, url_for, redirect, Blueprint, request,current_app,send_from_directory,abort
from . import db
from flask_login import login_required,current_user,logout_user
from . import dropzone
from .models import User,Upldoc
from werkzeug.utils import escape
upload = Blueprint('upload', __name__)
extension_img = ['jpeg','jpg','png']
extension_doc = ['txt','pdf','docx','jpeg','jpg','png']
upload_here = current_app.config['DEFAULT_UPLOAD_DIR']+'user_avatars/'
upload_docs = current_app.config['DEFAULT_UPLOAD_DIR']+'docs/'
def create_random_filename(filename,extension):
    '''Validate the filenames'''
    f = filename.split('.')
    if len(f) == 2:
        ext = f[1]
        if ext not in extension:
            return None
        ff = str(uuid4()) + "." + ext
        return str(ff)
    else:
        return None
@upload.route('/upload/avatar', methods=['POST'])
@login_required
def upload_avatar():
    if request.method == 'POST':
        File = request.files.get('file')
        f = create_random_filename(File.filename,extension_img)
        if (f):
            File.save(os.path.join(upload_here,f))
            u = User.query.filter_by(id=current_user.id).first()
            p = os.getcwd()+'/'+upload_here+u.avatar
            if os.path.exists(p) and u.avatar != 'defaultuser.png':
                os.remove(p)
            #removing previous image
            u.avatar = str(f)#change to new avatar location
            db.session.commit()
            
            return render_template('user_edit.html') 
        else:
            return "Failed to save the profile picture,Make sure image file should be in jpg or png format.",400
    else:
        return "Something went wrong.",400
@upload.route('/show/avatar',methods=['GET'])
@login_required
def show_avatar():#show the avatar fetch form database
    id = current_user.id
    if id != 0: # it means user is not anonymous
        u = User.query.filter_by(id = id ).first()
        return send_from_directory(current_app.config['USER_AVATAR_UPLOAD_DIR'],str(u.avatar))
    else:
        abort(404)
@upload.route('/switch/defaultpic')
@login_required
def switch_default():
    id = current_user.id
    if id != 0:
        u = User.query.filter_by(id=id).first()
        p = os.getcwd()+'/'+upload_here+u.avatar
        if os.path.exists(p) and u.avatar != 'defaultuser.png':
            os.remove(p)
            #removing previous image
        u.avatar = str('defaultuser.png')
        db.session.commit()
        flash('profile picture switch back to default,login again to reflect changes immediately.','green')
        return redirect(url_for('userprofile.useredit'))
@upload.route('/upload/form',methods=['POST'])
@login_required
def upload_form():
    title = escape(request.form.get('title'))
    desc = escape(request.form.get('description'))
    fl = request.files.get('doc')
    if title and desc and fl:
        f = create_random_filename(fl.filename,extension_doc)
        if f:
            fl.save(os.path.join(upload_docs,f))
            newdata = Upldoc(title=title,description=desc,doctype=str(fl.mimetype),location=str(f),userid=int(current_user.id))
            db.session.add(newdata)
            db.session.commit()
            flash('Uploaded successfull.','green')
            return redirect(url_for('main.index'))
        else:
            flash('Something wrong with file.','red')
            return redirect(url_for("main.index"))
    else:
        flash('Something went wrong.','red')
        return redirect(url_for('main.index'))
@upload.route('/download/doc/<string:filetodown>')
@login_required
def download_doc(filetodown):
    return send_from_directory(current_app.config['USER_DOCS_UPLOAD_DIR'],str(filetodown),as_attachment=True)

@upload.route('/show/doc/<string:filetoshow>')
@login_required
def show_doc(filetoshow):
    return send_from_directory(current_app.config['USER_DOCS_UPLOAD_DIR'],str(filetoshow),as_attachment=False)
@upload.route('/delete/doc/<int:id>')
@login_required
def delete_doc(id):
    userid = current_user.id
    if userid != 0:
        data = Upldoc.query.filter_by(id=id,userid=userid).first()
        p = os.getcwd() + '/' + upload_docs + str(data.location)
        if os.path.exists(p):
            os.remove(p)
        Upldoc.query.filter_by(id=id,userid=userid).delete()
        db.session.commit() 
        flash('Deleted successfull.','green')
        return redirect(url_for('main.index'))
    else:
        abort(404)
@upload.route('/edit/doc',methods=['POST'])
@login_required
def edit_doc():
    docid=int(escape(request.form.get('docid'))) 
    edittitle = str(escape(request.form.get('edittitle')))
    editdescription = str(escape(request.form.get('editdescription')))
    editfile = request.files.get('editdoc')
    if docid:
        data = Upldoc.query.filter_by(id=docid,userid=int(current_user.id)).first()
        # return redirect(url_for('main.index',showmessage=f"{edittitle}:{data.title} | {editdescription}:{data.description}"))
        if edittitle != data.title:
            data.title = edittitle
        if editdescription != data.description:
            data.description = editdescription
        if editfile:
            fl = create_random_filename(editfile.filename,extension_doc)
            if fl:
                # deleting the previous one
                p = os.getcwd() + '/' + upload_docs + str(data.location)
                if os.path.exists(p):
                    os.remove(p)
                editfile.save(os.path.join(upload_docs,fl))
                data.location = fl
                data.doctype = str(editfile.mimetype)
            else:
                flash('Something wrong with file.','red')
                return redirect(url_for('main.index'))
        db.session.commit() #commit changes
        flash('Editing successfull.','green')
        return redirect(url_for('main.index'))
    else:
        flash('Editing successfull.','red')
        return redirect(url_for('main.index'))
@upload.route('/switch_private/<int:docid>',methods=['GET'])
@login_required
def switch_private(docid):
    userid = current_user.id
    if userid != 0:
        data = Upldoc.query.filter_by(id=docid,userid=userid).first()
        data.private = True
        db.session.commit()
        return "Document switch to private successfully."
    return "Something went wrong."
@upload.route('/switch_public/<int:docid>',methods=['GET'])
@login_required
def switch_public(docid):
    userid = current_user.id
    if userid != 0:
        data = Upldoc.query.filter_by(id=docid,userid=userid).first()
        data.private = False
        db.session.commit()
        return "Document switch to public successfully."
    return "Something went wrong."