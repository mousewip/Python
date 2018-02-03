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
    return redirect('/panel/login')

# @app.route('/panel')
# @login_required
# def home():
#     # db.create_all()
#     print(current_user.username)
#     return redirect('/panel/' + current_user.username)

@app.route('/panel/user')
@login_required
def user():
    lstuser = User.query.all()
    return render_template('panel/user/detail.html', lstuser = lstuser)



@app.route('/panel/login', methods=['GET', 'POST'])
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

        return redirect('/panel/')
    return render_template('account/login.html', error_message = error_message)

@app.route('/panel/logout')
@login_required
def logout():
    logout_user()
    return redirect('/panel/login')


@app.route('/panel/user/check', methods=['POST'])
def check_username():
    uname = request.form['username'].lower()
    if(uname == "panel"):
        return "NOTOK"
    else:
        lstuser = User.query.filter_by(username = uname).all()
        print(len(lstuser))
        return "OK" if len(lstuser) == 0 else "NOTOK"

@app.route('/panel/user/checkemail', methods=['POST'])
def check_email():
    email = request.form['email'].lower()
    lstuser = User.query.filter_by(email = email).all()
    return "OK" if len(lstuser) == 0 else "NOTOK"


@app.route('/panel/register', methods=['POST'])
def register():
    uname = request.form['username'].lower()
    email = request.form['email']
    password = request.form['password']

    user = User(uname, email, password)
    db.session.add(user)
    db.session.commit()

    return redirect('/panel/login')

@app.route('/panel/')
@app.route('/panel/page/<page>')
@login_required
def get_entries(page = 1):
    per_page = request.args.get('limit', 10, type=int)
    lst_entry = Entry.query.filter(Entry.user_id == current_user.id).order_by(Entry.id).limit(per_page).offset(
        (int(page) - 1) * per_page).all()

    # lst_entry = Entry.query.order_by(Entry.id).limit(per_page).offset((page - 1) * per_page).all()

    if page == 1 and len(lst_entry) < per_page:
        total = len(lst_entry)
    else:
        total = Entry.query.filter(Entry.user_id == current_user.id).count()

    total_page = math.ceil(total / per_page)
    return render_template('admin/entry/detail.html', lstentry = lst_entry, total_page = total_page, page = int(page), limit = per_page)




@app.route('/post/<id>/edit', methods=['GET', 'POST'])
@login_required
def edit_post(id=None):
    entry = Entry.query.filter(Entry.id == id).first()
    if(request.method == 'GET'):
        if(entry.user_id == current_user.id):
            return render_template('admin/entry/edit.html', entry=entry)
        else:
            return redirect('/panel/')
    else:
        # eid = request.form['id']
        title = request.form['title']
        content = request.form['txtContent']
        description = request.form['description']
        # createdate = request.form['createdate']

        # entry = Entry.query.filter(Entry.id == eid).first()
        entry.title = title
        entry.content = content
        entry.teaser = description
        # entry.createdate = createdate

        db.session.commit()
        return redirect('/panel')

@app.route('/post/delete', methods=['POST'])
@login_required
def delete_post():
    id = request.form['id']
    entry = Entry.query.filter(Entry.id == id, Entry.user_id == current_user.id).first()

    if(entry is None):
        return "NOTOK"
    else:
        db.session.delete(entry)
        db.session.commit()
        return "OK"
