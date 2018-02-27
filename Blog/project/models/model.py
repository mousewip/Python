from project import app
import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, or_, BigInteger
from hashlib import md5
from flask.ext.login import UserMixin, LoginManager,  login_user, current_user, login_required, logout_user
import re
from unicodedata import normalize

db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "admin/login"


_punct_re = re.compile(r'[\t !"#$%&\'()*\-/<=>?@\[\\\]^_`{|},.+]+')
def slugify(text, delim=b'-'):
    """Generates an slightly worse ASCII-only slug."""
    result = []
    for word in _punct_re.split(text.lower()):
        word = normalize('NFKD', word).encode('ascii', 'ignore')
        if word:
            result.append(word)
    return str(delim.join(result), 'utf-8')



class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, nullable=False, unique=True)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    description = Column(String(1024), default=None)
    avatar = Column(String(250), default=None)
    cover = Column(String(250), default=None)
    facebook_id = Column(BigInteger, default=None)
    phone = Column(String(20), default=None)
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
    title = Column(String(250))
    description = Column(String(1024))
    metatitle = Column(String(250))
    content = Column(Text)
    image = Column(String(250), default=None)
    views = Column(Integer, default=0)
    createdate = Column(DateTime, default=datetime.datetime.now)
    user_id = Column(Integer, ForeignKey('user.id'), default=None, nullable=False)
    status = Column(Integer, default=1)
    posttag = db.relationship('PostTag', backref='entries', lazy=True)
    category_id = Column(Integer, ForeignKey('category.id'), nullable=False)

    def __init__(self, title, description, content, category_id, image, user_id=1):
        self.title = title
        self.description = description
        self.metatitle = slugify(title)
        self.content = content
        self.user_id = user_id
        self.image = image
        self.category_id = category_id


class Category(db.Model):
    __tablename__ = 'category'
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(250))
    metatitle = Column(String(250))
    posts = db.relationship('Entry', backref='category', lazy=True)

    def __init__(self, title):
        self.title = title
        self.metatitle = slugify(title)

class Tag(db.Model):
    __tablename__ = 'tags'
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(100))
    metatitle = Column(String(100))
    posttag = db.relationship('PostTag', backref='tags', lazy=True)

    def __init__(self, title):
        self.title = title
        self.metatitle = slugify(title)

class PostTag(db.Model):
    __tablename__ = 'posttags'
    id = Column(Integer, primary_key=True, autoincrement=True)
    postid = Column(Integer, ForeignKey('entries.id'), nullable=False)
    tagid = Column(Integer, ForeignKey('tags.id'), nullable=False)

    def __init__(self, entry_id, tag_id):
        self.postid = entry_id
        self.tagid = tag_id

