# -*- coding: utf-8 -*-

from project import app
from project.models.model import *
from flask import render_template, request, redirect, json, url_for
import math, base64
from project.controllers.helper import *
import os
from werkzeug.utils import secure_filename


@app.context_processor
def load_category():
    lst_category = Category.query.all()
    return dict(lstcategory=lst_category)


@app.template_filter('custom_encode')
def encode_processor(id):
    return hash_id_encode(id)


@app.template_filter('counter_category')
def counter_processor(id):
    return Entry.query.filter(Entry.category_id == id).count()


@app.errorhandler(404)
def page_not_found(e):
    return render_template('post/notfound.html')


@app.route('/')
@app.route('/page/<page>')
def home(page=1):
    # db.drop_all()
    # db.create_all()
    per_page = request.args.get('limit', 10, type=int)

    lst_entry = Entry.query.filter(Entry.status == 1) \
        .order_by(Entry.id.desc()).limit(per_page) \
        .offset((int(page) - 1) * per_page).all()
    if page == 1 and len(lst_entry) < per_page:
        total = len(lst_entry)
    else:
        total = Entry.query.filter(Entry.status == 1).count()

    total_page = math.ceil(total / per_page)
    result = {
        'lstentry': lst_entry,
        'total_page': total_page,
        'page': int(page),
        'limit': per_page
    }
    return render_template('home/index.html', result=result)


@app.route('/<uname>')
@app.route('/<uname>/page/<page>')
def user_blog(uname, page=1):
    per_page = request.args.get('limit', 10, type=int)

    user = User.query.filter(User.username == uname).first_or_404()
    lst_tmp = Entry.query \
        .filter(Entry.user_id == user.id) \
        .order_by(Entry.id.desc())
    if (hasattr(current_user, 'id') and user.id == current_user.id):
        lst_entry = lst_tmp.limit(per_page).offset((int(page) - 1) * per_page).all()
    else:
        lst_entry = lst_tmp.filter(Entry.status == 1).limit(per_page).offset((int(page) - 1) * per_page).all()

    if page == 1 and len(lst_entry) < per_page:
        total = len(lst_entry)
    else:
        if (hasattr(current_user, 'id') and user.id == current_user.id):
            total = Entry.query.filter(Entry.user_id == user.id).count()
        else:
            total = Entry.query.filter(Entry.user_id == user.id, Entry.status == 1).count()

    total_page = math.ceil(total / per_page)
    result = {
        'lstentry': lst_entry,
        'total_page': total_page,
        'page': int(page),
        'username': uname,
        'limit': per_page
    }
    if (hasattr(current_user, 'id') and user.id == current_user.id):
        return render_template('home/my_blog.html', result=result)
    else:
        return render_template('home/user_post.html', result=result)


@app.route('/category/<url>-<id>/page/<page>')
@app.route('/category/<url>-<id>')
def category(url, id, page=1):
    c_id = has_id_decode(id)

    per_page = request.args.get('limit', 10, type=int)
    lst_post = Entry.query.filter(Entry.category_id == c_id, Entry.status == 1) \
        .order_by(Entry.id.desc()) \
        .limit(per_page).offset((int(page) - 1) * per_page).all()

    if page == 1 and len(lst_post) < per_page:
        total = len(lst_post)
    else:
        total = Entry.query.filter(Entry.category_id == c_id, Entry.status == 1).count()
    total_page = math.ceil(total / per_page)
    result = {
        'lstentry': lst_post,
        'total_page': total_page,
        'page': int(page),
        'limit': per_page,
        'url': url,
        'id': c_id
    }

    return render_template('home/category.html', result=result)


@app.route('/search', methods=['POST', 'GET'])
@app.route('/search/page/<page>', methods=['POST', 'GET'])
def search(page=1):
    per_page = request.args.get('limit', 10, type=int)
    r = request.args.get('r', type=str)

    lst_entry = Entry.query.filter(Entry.status == 1) \
        .filter(
        or_(Entry.title.like('%' + r + '%'), Entry.description.like('%' + r + '%'), Entry.content.like('%' + r + '%'))) \
        .order_by(Entry.id.desc()).limit(per_page) \
        .offset((int(page) - 1) * per_page).all()
    if page == 1 and len(lst_entry) < per_page:
        total = len(lst_entry)
    else:
        total = Entry.query.filter(Entry.status == 1).count()

    total_page = math.ceil(total / per_page)
    result = {
        'lstentry': lst_entry,
        'total_page': total_page,
        'page': int(page),
        'limit': per_page
    }
    return render_template('home/index.html', result=result)


@app.route('/tags/listtags', methods=['POST'])
@login_required
def load_list_tags():
    if request.form['tags_list'] == 'get_data':
        lst_tags = []
        tags = Tag.query.all()
        [lst_tags.append(tag.title) for tag in tags]
        return json.dumps(lst_tags)
    else: pass
