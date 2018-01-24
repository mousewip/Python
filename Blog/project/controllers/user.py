# -*- coding: utf-8 -*-

from project import app
from project.models.model import *
from flask import render_template, request, redirect, jsonify, json, url_for
import math


@app.route('/')
def main_page():
    # db.drop_all()
    db.create_all()


    per_page = 10
    page = 1
    lst_entry = Entry.query.order_by(Entry.id).limit(per_page).offset((page - 1) * per_page).all()

    if page == 1 and len(lst_entry) < per_page:
        total = len(lst_entry)
    else:
        total = Entry.query.count()

    total_page = math.ceil(total / per_page)
    print(total_page)

    print(total)


    return render_template('user/home/index.html', lstentry = lst_entry, total_page = total_page, page = page)


@app.route('/entry/<id>')
def entry_detail(id):
    # entri_id = request
    entry = Entry.query.filter(Entry.id == id).first()
    return render_template('user/entry/index.html', entry=entry)
