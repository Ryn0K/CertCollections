from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager,current_user,AnonymousUserMixin
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_dropzone import Dropzone
from flask_wtf.csrf import CSRFProtect,CSRFError
db = SQLAlchemy()
csrf = CSRFProtect()


# from flask factory pattern of application context
dropzone = Dropzone() # initialise the dropzone app
'''When there is no login session or user not loggedin.'''
class Anonymous(AnonymousUserMixin):
	def __init__(self):
		'''Setting default values for anonymous user'''
		self.admin = False 
		self.id = 0 

def create_app():
	app = Flask(__name__)
	with app.app_context():
		app.config.from_pyfile('../config.py') # load configuration from file
		db.init_app(app) # initialize app to use with database
		dropzone.init_app(app)# initialize the dropzone
		csrf.init_app(app)

		login_manager = LoginManager()
		login_manager.login_view = 'auth.login'
		login_manager.anonymous_user = Anonymous
		login_manager.init_app(app)

		from .models import User

		@login_manager.user_loader

		def load_user(user_id):
			return User.query.get(int(user_id))

		from .auth import auth as auth_blueprint
		app.register_blueprint(auth_blueprint)

		from .main import main as main_blueprint
		app.register_blueprint(main_blueprint)

		from .userprofile import userprofile as userprofile_blueprint
		app.register_blueprint(userprofile_blueprint)
		
		from .reportissue import report as report_blueprint
		app.register_blueprint(report_blueprint)

		from .admin import SetFlaskAdmin
		SetFlaskAdmin(app) # providing app object to flaskadmin function

		from .upload import upload as upload_blueprint
		app.register_blueprint(upload_blueprint)
		
		from .publicprofile import publicprofile as publicprofile_blueprint
		app.register_blueprint(publicprofile_blueprint)
		@app.errorhandler(CSRFError)
		def handle_csrf_error(e):
			return 'CSRF validation failed',400
	return app