# -*- coding: utf-8 -*-

from project import app, mail
from project.models.model import *
from project.controllers.helper import *
from flask import render_template, request, redirect, jsonify, json
import babel, random
import os
from flask_mail import Mail, Message

root = os.path.dirname(__file__)[:-12].strip()
user_path = os.path.join(root, "static/upload")


def format_datetime(value, format='medium'):
    if format == 'full':
        format = "EEEE, d. MMMM y 'at' HH:mm"
    elif format == 'medium':
        format = "EE dd.MM.y HH:mm"
    return babel.dates.format_datetime(value, format)


app.jinja_env.filters['datetime'] = format_datetime


@login_manager.user_loader
def load_user(user_name):
    return User.query.get(user_name)


# redirect to login view - login_required
@login_manager.unauthorized_handler
def unauthorized():
    return redirect('/login')


@app.route('/profile')
@login_required
def profile():
    return render_template('account/profile.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    error_message = ''
    if request.method == 'POST':
        username = request.form['username']
        password = md5(request.form['password'].encode()).hexdigest()

        user = User.query.filter_by(username=username, password=password).first()
        if (user):
            login_user(user=user)
        else:
            error_message = 'Wrong User Name or Password!'

    if current_user.is_authenticated:
        return redirect('/' + current_user.username)

    return render_template('account/login.html', error_message=error_message)


@app.route('/loginfb', methods=['POST'])
def loginfb():
    error_message = ''
    response = {}
    print('call loginfb')
    if request.method == 'POST':
        fid = request.form['f_']
        email = request.form['e_']
        torken = request.form['t_']

        user = User.query.filter_by(facebook_id=fid).first()
        if (user):
            login_user(user=user)
        else:
            error_message = 'Wrong User Name or Password!'

    if current_user.is_authenticated:
        response['code'] = 200
        response['message'] = error_message
    else:
        response['code'] = 201
        response['message'] = error_message
    return json.dumps(response)




@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/login')


@app.route('/account/checkusername', methods=['POST'])
def check_username():
    uname = request.form['username'].lower()
    lstuser = User.query.filter_by(username=uname).all()
    response = {}
    if (len(lstuser) == 0):
        response['code'] = 200
        response['message'] = ''
    else:
        response['code'] = 201
        response['message'] = 'Username already taken!'
    return json.dumps(response)


@app.route('/account/checkemail', methods=['POST'])
def check_email():
    email = request.form['email'].lower()
    lstuser = User.query.filter_by(email=email).all()
    response = {}
    if (len(lstuser) == 0):
        response['code'] = 200
        response['message'] = ''
    else:
        response['code'] = 201
        response['message'] = 'This email address is already associated with an account.'
    return json.dumps(response)

@app.route('/account/checkfid', methods=['POST'])
def check_facebook_id():
    fid = request.form['f_']
    email = request.form['e_']
    lstuser = User.query.filter(or_(User.facebook_id==fid, User.email==email)).all()
    response = {}
    if (len(lstuser) == 0):
        response['code'] = 200
        response['message'] = ''
    elif lstuser[0].facebook_id is not None:
        response['code'] = 201
    elif lstuser[0].facebook_id is None:
        response['code'] = 202
        response['message'] = 'This email address is already associated with an account.'

    return json.dumps(response)


@app.route('/register', methods=['POST'])
def register():
    uname = request.form['username'].lower()
    email = request.form['email']
    password = request.form['password']

    response = {}
    if uname == "" or email == "" or password == "":
        response['code'] = 201
        response['message'] = 'Register fail, some field is empty, try again!'
        return json.dumps(response)
    user = User(uname, email, password)
    try:
        db.session.add(user)
        db.session.commit()
        response['code'] = 200
        response['message'] = 'Register success. Login now!'

        try:
            full_path = os.path.join(user_path, uname)
            os.mkdir(full_path)
        except Exception as e:
            response['code'] = 201
            response['message'] = 'Register fail, ' + str(e) + ', try again!'
    except Exception as ey:
        response['code'] = 201
        response['message'] = 'Register fail, ' + str(ey) + ', try again!'

    return json.dumps(response)


@app.route('/registerfb', methods=['POST'])
def registerfb():
    fid = request.form['f_']
    uname = request.form['u_']
    email = request.form['e_']
    torken = request.form['t_']

    response = {}
    if fid == "" or email == "" or torken == "" or uname == "":
        response['code'] = 201
        response['message'] = 'Register fail, some field is empty, try again!'
        return json.dumps(response)
    user = User(uname, email, torken)
    user.password = torken
    user.facebook_id = fid

    try:
        db.session.add(user)
        db.session.commit()
        response['code'] = 200
        response['message'] = 'Register success. Login now!'

        try:
            full_path = os.path.join(user_path, uname)
            os.mkdir(full_path)
        except Exception as e:
            response['code'] = 201
            response['message'] = 'Register fail, ' + str(e) + ', try again!'
    except Exception as ey:
        response['code'] = 201
        response['message'] = 'Register fail, ' + str(ey) + ', try again!'

    return json.dumps(response)


@app.route('/subscribe', methods=['POST'])
def subscribe():
    email = request.form['email']
    type = request.form['type']
    result = {}

    if (type == 'subscribe'):
        result['code'] = 200
        result['message'] = 'Subscribe success!'
    elif type == 'unsubscribe':
        result['code'] = 200
        result['message'] = 'Unsubscribe success!'
    return json.dumps(result)


@app.route('/forgetpassword', methods=['POST'])
def forgetpassword():
    email = request.form['email']
    result = {}

    n_pass = random.randint(0, 999999)
    n_pass_encode = hash_id_encode(n_pass)
    md5_pass_encode = md5(n_pass_encode.encode()).hexdigest()

    user = User.query.filter_by(email=email).first()
    if user is not None:
        user.password = md5_pass_encode
        db.session.commit()
        f = open(root + '/static/mail.html', 'r')
        body = f.read()

        a = body.replace('{{USER}}', user.username)
        b = a.replace('{{PASSWORD}}', n_pass_encode)

        msg = Message('Reset password', recipients=[user.email])
        msg.html = b
        try:
            mail.send(msg)
            result['code'] = 200
            result['message'] = 'New password will be send to your emai, please check email!'
        except Exception as e:
            result['code'] = 201
            result['message'] = str(e)
    else:
        result['code'] = 201
        result['message'] = 'No account associated with an email!'


    return json.dumps(result)

@app.route('/change_password', methods=['POST'])
@login_required
def change_password():
    oldpass = md5(request.form['oldpass'].encode()).hexdigest()
    newpass = md5(request.form['newpass'].encode()).hexdigest()
    repass = md5(request.form['repass'].encode()).hexdigest()

    result = {}
    user = User.query.filter(User.id == current_user.id).first()
    if oldpass != user.password:
        result['code'] = 201
        result['message'] = "Input password doesn't match current password."
    elif newpass != repass:
        result['code'] = 201
        result['message'] = "Confirm password does not match the password."
    else:
        user.password = newpass
        db.session.commit()
        result['code'] = 200
        result['message'] = "Change password success."
    return json.dumps(result)
