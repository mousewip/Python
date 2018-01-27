# -*- coding: utf-8 -*-

from project import app
from project.models.model import *
from flask import render_template, request, redirect, jsonify, json, url_for
import math
from sqlalchemy.orm import joinedload




@app.route('/')
@app.route('/page/<page>')
def main_page(page = 1):
    # db.drop_all()
    # db.create_all()
    per_page = request.args.get('limit', 10, type=int)

    lst_entry  = Entry.query.join(User, Entry.user_id == User.id).order_by(Entry.id).limit(per_page).offset((int(page) - 1) * per_page).all()
    if page == 1 and len(lst_entry) < per_page:
        total = len(lst_entry)
    else:
        total = Entry.query.count()

    total_page = math.ceil(total / per_page)
    print(total_page)
    print(total)
    return render_template('user/home/index.html', lstentry = lst_entry, total_page = total_page, page = int(page), limit = per_page)


@app.route('/<uname>/entry/<id>')
def entry_detail(uname, id):
    # entri_id = request
    user = User.query.filter(User.username == uname).first_or_404()
    entry = Entry.query.filter(Entry.id == id , Entry.user_id == user.id).first_or_404()
    return render_template('user/entry/index.html', entry=entry)

@app.route('/<uname>')
@app.route('/<uname>/page/<page>')
@app.route('/<uname>/entry')
@app.route('/<uname>/entry/page/<page>')
def user_entry(uname, page = 1):
    per_page = request.args.get('limit', 10, type=int)

    user = User.query.filter(User.username == uname).first_or_404()
    lst_entry = Entry.query.filter(Entry.user_id == user.id).order_by(Entry.id).limit(per_page).offset((int(page) - 1) * per_page).all()

    if page == 1 and len(lst_entry) < per_page:
        total = len(lst_entry)
    else:
        total = Entry.query.filter(Entry.user_id == user.id).count()

    total_page = math.ceil(total / per_page)
    return render_template('user/entry/user_entry.html', lstentry=lst_entry, total_page = total_page, page = int(page), username = uname, limit = per_page)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('user/entry/notfound.html')