SECRET_KEY = "ThisisRyn0"
SQLALCHEMY_DATABASE_URI = "sqlite:///db.sqlite3"
MAX_CONTENT_LENGTH=16 * 1024 * 1024
DEFAULT_UPLOAD_DIR = 'uploads/'
USER_AVATAR_UPLOAD_DIR= '../uploads/user_avatars/'
USER_DOCS_UPLOAD_DIR = '../uploads/docs/'
DROPZONE_ALLOWED_FILE_CUSTOM = True
DROPZONE_ALLOWED_FILE_TYPE= ['image/*, .pdf, .txt']