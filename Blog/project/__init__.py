# -*- coding: utf-8 -*-
__version__ = '1.0'
from flask import Flask
# from flask.ext.uploads import UploadSet, configure_uploads, IMAGES
from flask_mail import Mail, Message

app = Flask('project')
app.config['SECRET_KEY'] = 'c6c482b268b0a985f9b19c03419e246a'
app.config.from_pyfile('config.cfg')
UPLOAD_FOLDER = '/static/upload/'

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'mousewip@gmail.com'
app.config['MAIL_DEFAULT_SENDER'] = 'mousewip@gmail.com'
app.config['MAIL_PASSWORD'] = 'rghmeucprdsbncuv'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

app.debug = True
mail = Mail(app)
#
#
#
# photos = UploadSet('photos', IMAGES)
# app.config['UPLOADED_PHOTOS_DEST'] = 'static/img'
# configure_uploads(app, photos)

from project.controllers import *
