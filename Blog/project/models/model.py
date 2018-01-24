from project import app
import datetime
from flask_migrate import Migrate, MigrateCommand, Manager
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, DateTime, Text
from hashlib import md5
from flask.ext.login import UserMixin, LoginManager,  login_user, current_user, login_required, logout_user
from flask import Flask

# app = Flask('project')
# app.config['SECRET_KEY'] = 'blogfull'
# app.config.from_pyfile('config.cfg')
# app.debug = True

# app.secret_key = 'c6c482b268b0a985f9b19c03419e246a'

db = SQLAlchemy(app)

# migrate = Migrate(app=app,db=db)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "admin/login"



class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, nullable=False, unique=True)
    email = Column(String, nullable=False)
    password = Column(String, nullable=False)

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
    content = Column(Text)
    createdate = Column(DateTime, default = datetime.datetime.now)

    def __init__(self, title, content):
        self.title = title
        self.content = content

# if __name__ == '__main__':
#     manager.run()