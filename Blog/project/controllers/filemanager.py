from flask import request, jsonify
from project.models.model import *
from project.models.logic import CkFinder
from flask import render_template

@app.route('/filemanager/manager/', methods=['POST', 'GET'])
def get_info():
    if(request.method == 'POST'):
        ckfinder = CkFinder()
        upload_path = request.form.get('currentpath', '')
        new_file = request.files['newfile']
        return ckfinder.upload(upload_path, new_file)
    else:
        ckfinder = CkFinder()
        action = request.args.get('mode', '')
        if "getinfo" == action:
            info = ckfinder.get_info(request.args.get("path", ""))
            return jsonify(info)

        elif "getfolder" == action:
            return jsonify(ckfinder.get_dir_file(request.args.get("path", "")))

        elif "rename" == action:
            old_name = request.args.get("old", "")
            new_name = request.args.get("new", "")
            return ckfinder.rename(old_name, new_name)

        elif "delete" == action:
            path = request.args.get("path", "")
            return ckfinder.delete(path)

        elif "addfolder" == action:
            path = request.args.get("path", "")
            name = request.args.get("name", "")
            return ckfinder.addfolder(path, name)

        else:
            return "fail"

@app.route('/filemanager/manager/dirlist/', methods=['POST'])
def dir_info():
    ckfinder = CkFinder()
    return ckfinder.dir_list(request)

@app.route('/filemanager/browser/')
def file_browser():
    return render_template('/layout/index.html')
