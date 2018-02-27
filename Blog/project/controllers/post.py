from project import app
from project.models.model import *
from flask import render_template, request, redirect, json, url_for
from project.controllers.helper import *
import os
from werkzeug.utils import secure_filename
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

root = os.path.dirname(__file__)[:-12].strip()
user_path = os.path.join(root, "static\\upload")


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.context_processor
def load_top_post():
    lst_entry = Entry.query.filter(Entry.status == 1) \
        .order_by(Entry.views.desc()) \
        .limit(10).offset(0).all()
    return dict(lst_top_entry=lst_entry)


@app.context_processor
def load_latest_post():
    lst_entry = Entry.query.filter(Entry.status == 1).order_by(Entry.id.desc()).limit(3).offset(0).all()
    return dict(lst_latest_post=lst_entry)


@app.context_processor
def load_older_post():
    lst_entry = Entry.query.filter(Entry.status == 1).order_by(Entry.id.asc()).limit(3).offset(0).all()
    return dict(lst_older_post=lst_entry)

@app.context_processor
def load_list_tag():
    lst_tag = Tag.query.all()
    lst_tag.sort(key=lambda item: (item.title, item.title))
    return dict(lst_tag=lst_tag)


@app.route('/<uname>/post/<url>-<id>.html')
def entry_detail(uname, url, id):
    e_id = has_id_decode(id)
    user = User.query.filter(User.username == uname).first_or_404()
    if hasattr(current_user, 'id') and user.id == current_user.id:
        entry = Entry.query.filter(Entry.id == e_id, Entry.user_id == user.id).first_or_404()
    else:
        entry = Entry.query.filter(Entry.id == e_id, Entry.user_id == user.id, Entry.status == 1).first_or_404()
    entry.views += 1
    db.session.commit()

    latests = Entry.query.filter(Entry.status == 1, Entry.user_id == user.id).order_by(Entry.id.desc()).limit(3).offset(0).all()
    return render_template('post/detail.html', entry=entry, user=user, latests = latests)


@app.route('/post/add', methods=['GET', 'POST'])
@login_required
def add_post():
    if (request.method == 'GET'):
        return render_template('post/add.html')
    else:
        category_id = request.form['categoryId']
        title = request.form['title']
        content = request.form['content']
        description = request.form['description']
        publish = request.form.get('publish')
        tags = request.form.get('tags')
        link = ""

        # save image
        # check if the post request has the file part
        if 'image' not in request.files:
            return redirect(request.url)
        file = request.files['image']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            link = current_user.username + "/" + filename
            file.save(os.path.join(user_path, current_user.username, filename))

        # add entry
        entry = Entry(title, description, content, int(category_id), link, current_user.id)
        db.session.add(entry)
        db.session.commit()

        # add tags & post tag
        lst_tags = tags.split(',')
        for tag in lst_tags:
            tag_tmp = Tag.query.filter_by(title=tag).first()
            if tag_tmp is None:
                # add tag
                t = Tag(tag)
                db.session.add(t)
                db.session.commit()
                # add post tag
                pt = PostTag(entry.id, t.id)
                db.session.add(pt)
                db.session.commit()
            else:
                pt = PostTag(entry.id, tag_tmp.id)
                db.session.add(pt)
                db.session.commit()

        return redirect('/')

@app.route('/post/<id>/edit', methods=['GET', 'POST'])
@login_required
def edit_post(id=None):
    p_id = has_id_decode(id)
    entry = Entry.query.filter(Entry.id == p_id, Entry.user_id == current_user.id).first_or_404()
    if (request.method == 'GET'):
        if (entry.user_id == current_user.id):
            lst_tags = []
            posttags = PostTag.query.filter_by(postid=entry.id).all()
            [lst_tags.append(tag.tags.title) for tag in posttags]
            return render_template('post/edit.html', entry=entry, lst_tags = lst_tags)
        else:
            return redirect(url_for('home', page=1))
    else:
        category_id = request.form['categoryId']
        title = request.form['title']
        content = request.form['content']
        description = request.form['description']
        publish = request.form.get('publish')
        tags = request.form.get('tags')
        url_image = request.form['link-image']
        link = ""
        if url_image != entry.image:
            # check if the post request has the file part
            if 'image' not in request.files:
                return redirect(request.url)
            file = request.files['image']
            # if user does not select file, browser also
            # submit a empty part without filename
            if file.filename == '':
                return redirect(request.url)
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                link = current_user.username + "/" + filename
                file.save(os.path.join(user_path, current_user.username, filename))

        posttags = PostTag.query.filter_by(postid=entry.id).all()

        lst_tags = tags.split(',') if tags is not None else []
        for tag in posttags:
            if tag.tags.title not in lst_tags:
                db.session.delete(tag)
                db.session.commit()

        for tag in lst_tags:
            tag_tmp = Tag.query.filter_by(title=tag).first()
            if tag_tmp is None:
                # add tag
                t = Tag(tag)
                db.session.add(t)
                db.session.commit()
                # add post tag
                pt = PostTag(entry.id, t.id)
                db.session.add(pt)
                db.session.commit()
            else:
                # Check Post tag is already exists, if not exists add new
                pt = PostTag.query.filter_by(postid=entry.id, tagid=tag_tmp.id).first()
                if pt is None:
                    pt = PostTag(entry.id, tag_tmp.id)
                    db.session.add(pt)
                    db.session.commit()



        entry.description = description
        entry.content = content
        entry.title = title
        entry.metatitle = slugify(title)
        entry.category_id = category_id
        entry.status = 1 if publish else 0

        db.session.commit()
        return redirect(url_for('entry_detail', uname=current_user.username, url=entry.metatitle, id = id))


@app.route('/post/delete', methods=['POST'])
@login_required
def delete_post():
    id = request.form['id']
    entry = Entry.query.filter(Entry.id == id, Entry.user_id == current_user.id).first()
    response = {}
    if (entry is None):
        response['code'] = 202
        response['message'] = 'Access is denied'
    else:
        try:
            # delete post tag first, dependency of Entry
            db.session.query(PostTag).filter(PostTag.postid == entry.id).delete()
            db.session.commit()

            db.session.delete(entry)
            db.session.commit()
            response['code'] = 200

            response['message'] = 'Delete Success'
        except Exception as e:
            db.session.rollback()
            response['code'] = 201
            response['message'] = str(e)
    return json.dumps(response)


@app.route('/post/changestatus', methods=['POST'])
@login_required
def change_status_post():
    id = request.form['id']
    entry = Entry.query.filter(Entry.id == id, Entry.user_id == current_user.id).first()
    response = {}
    if (entry is None):
        response['code'] = 202
        response['message'] = 'Access is denied'
    else:
        try:
            entry.status = 0 if entry.status else 1
            db.session.commit()
            response['code'] = 200

            mess = "This post is publish." if entry.status else "This post is Unpublish."

            response['message'] = mess
        except Exception as e:
            response['code'] = 201
            response['message'] = str(e)
    return json.dumps(response)
