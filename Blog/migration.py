from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from sqlalchemy import Column,Integer,String, Text, DateTime, ForeignKey
import datetime
from hashlib import md5

app = Flask(__name__)
app.config.from_pyfile('project/config.cfg')

db = SQLAlchemy(app)

migrate = Migrate(app=app,db=db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)


class User(db.Model):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, nullable=False, unique=True)
    email = Column(String, nullable=False)
    password = Column(String, nullable=False)

    entries = db.relationship('Entry', backref='user', lazy=True)

    def __init__(self, uname, email, password):
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

    def __init__(self, title,teaser, content, user_id = 1):
        self.title = title
        self.teaser = teaser
        self.content = content
        self.user_id = user_id

if __name__ == '__main__':
    manager.run()
