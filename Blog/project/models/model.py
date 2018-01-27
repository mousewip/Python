from project import app
import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey
from hashlib import md5
from flask.ext.login import UserMixin, LoginManager,  login_user, current_user, login_required, logout_user

db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "admin/login"



class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, nullable=False, unique=True)
    email = Column(String, nullable=False)
    password = Column(String, nullable=False)

    entries = db.relationship('Entry', backref='user', lazy=True)

    def __init__(self, uname, email ,password):
        self.username = uname
        self.email = email
        self.set_password(password)

    def set_password(self, password):
        self.password = md5(password.encode()).hexdigest()

class Entry(db.Model):
    __tablename__ = 'entries'
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(1024))
    teaser = Column(String(1024))
    content = Column(Text)
    createdate = Column(DateTime, default=datetime.datetime.now)
    user_id = Column(Integer, ForeignKey('user.id'), default=None, nullable=False)

    def __init__(self, title, description, content, user_id=1):
        self.title = title
        self.teaser = description
        self.content = content
        self.user_id = user_id
