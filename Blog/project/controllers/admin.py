# -*- coding: utf-8 -*-

from project import app
from project.models.model import *
from flask import render_template, request, redirect, jsonify, json
import babel
import math

def format_datetime(value, format='medium'):
    if format == 'full':
        format="EEEE, d. MMMM y 'at' HH:mm"
    elif format == 'medium':
        format="EE dd.MM.y HH:mm"
    return babel.dates.format_datetime(value, format)

app.jinja_env.filters['datetime'] = format_datetime

@login_manager.user_loader
def load_user(user_name):
    return User.query.get(user_name)

# redirect to login view - login_required
@login_manager.unauthorized_handler
def unauthorized():
    return redirect('/admin/login')

@app.route('/admin')
@login_required
def home():
    db.create_all()
    return render_template('admin/home/index.html')

@app.route('/admin/user')
@login_required
def user():
    lstuser = User.query.all()
    return render_template('admin/user/index.html', lstuser = lstuser)



@app.route('/admin/login', methods=['GET', 'POST'])
def login():
    error_message = ''
    if(request.method == 'POST'):
        username = request.form['username']
        password = md5(request.form['password'].encode()).hexdigest()

        user = User.query.filter_by(username = username, password = password).first()
        if (user):
            login_user(user = user)
        else: error_message = 'Wrong User Name or Password!'

    if (current_user.is_authenticated):
        print(current_user.id)

        return redirect('/admin')
    return render_template('admin/login/index.html', error_message = error_message)

@app.route('/admin/logout')
@login_required
def logout():
    logout_user()
    return redirect('/admin/login')


@app.route('/admin/register', methods=['POST'])
def register():
    uname = request.form['username']
    email = request.form['email']
    password = request.form['password']

    user = User(uname, email, password)
    db.session.add(user)
    db.session.commit()

    return redirect('/admin/login')

@app.route('/admin/entry')
@login_required
def get_entries():
    per_page = 10
    page = 1
    lst_entry = Entry.query.order_by(Entry.id).limit(per_page).offset((page - 1) * per_page).all()

    if page == 1 and len(lst_entry) < per_page:
        total = len(lst_entry)
    else:
        total = Entry.query.count()

    total_page = math.ceil(total / per_page)
    return render_template('admin/entry/index.html', lstentry = lst_entry, total_page = total_page, page = page)

@app.route('/admin/entry/add', methods=['GET', 'POST'])
@login_required
def add_entries():
    if(request.method == 'GET'):
        return render_template('admin/entry/add.html')
    else:
        title = request.form['title']
        content = request.form['txtContent']

        entry = Entry(title, content)
        db.session.add(entry)
        db.session.commit()
        return redirect('/admin/entry')


@app.route('/admin/entry/<id>/edit', methods=['GET', 'POST'])
@login_required
def edit_entries(id=None):
    entry = Entry.query.filter(Entry.id == id).first()
    if(request.method == 'GET'):
        return render_template('admin/entry/edit.html', entry=entry)
    else:
        # eid = request.form['id']
        title = request.form['title']
        content = request.form['txtContent']
        # createdate = request.form['createdate']

        # entry = Entry.query.filter(Entry.id == eid).first()
        entry.title = title
        entry.content = content
        # entry.createdate = createdate

        db.session.commit()
        return redirect('/admin/entry')
