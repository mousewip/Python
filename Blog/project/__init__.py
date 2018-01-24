# -*- coding: utf-8 -*-
__version__ = '1.0'
from flask import Flask

app = Flask('project')
app.config['SECRET_KEY'] = 'blogfull'
app.config.from_pyfile('config.cfg')
app.debug = True

from project.controllers import *
