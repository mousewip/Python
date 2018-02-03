# -*- coding: utf-8 -*-

from project import app
from project.models.model import *
from flask import render_template, request, redirect, jsonify, json, url_for
import math, base64
from sqlalchemy.orm import joinedload
import jinja2

app.jinja_env.filters['b64encode'] = base64.b64encode

@app.route('/')
@app.route('/page/<page>')
def home(page = 1):
    # db.drop_all()
    # db.create_all()
    per_page = request.args.get('limit', 9, type=int)

    lst_entry  = Entry.query.join(User, Entry.user_id == User.id).order_by(Entry.id).limit(per_page).offset((int(page) - 1) * per_page).all()
    if page == 1 and len(lst_entry) < per_page:
        total = len(lst_entry)
    else:
        total = Entry.query.count()

    total_page = math.ceil(total / per_page)
    print(total_page)
    print(total)
    return render_template('home/index.html', lstentry = lst_entry, total_page = total_page, page = int(page), limit = per_page)


@app.route('/<uname>/entry/<url>-<id>.html')
def entry_detail(uname,url, id):
    # entri_id = request
    user = User.query.filter(User.username == uname).first_or_404()
    entry = Entry.query.filter(Entry.id == id , Entry.user_id == user.id).first_or_404()
    return render_template('entry/notfound.html', entry=entry, user = user)

@app.route('/<uname>')
@app.route('/<uname>/page/<page>')
@app.route('/<uname>/entry')
@app.route('/<uname>/entry/page/<page>')
def user_entry(uname, page = 1):
    per_page = request.args.get('limit', 9, type=int)

    user = User.query.filter(User.username == uname).first_or_404()
    lst_entry = Entry.query.filter(Entry.user_id == user.id).order_by(Entry.id).limit(per_page).offset((int(page) - 1) * per_page).all()

    if page == 1 and len(lst_entry) < per_page:
        total = len(lst_entry)
    else:
        total = Entry.query.filter(Entry.user_id == user.id).count()

    total_page = math.ceil(total / per_page)
    return render_template('entry/user_entry.html', lstentry=lst_entry, total_page = total_page, page = int(page), username = uname, limit = per_page)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('entry/notfound.html')


@app.route('/post/add', methods=['GET', 'POST'])
@login_required
def add_post():
    if(request.method == 'GET'):
        return render_template('entry/add.html')
    else:
        title = request.form['title']
        content = request.form['txtContent']
        description = request.form['description']

        entry = Entry(title, description, content, current_user.id)
        db.session.add(entry)
        db.session.commit()
        return redirect('/panel')