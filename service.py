#!/usr/bin/env python3
import difflib
import json
import os

from flask import Flask, request
from werkzeug.utils import secure_filename

from nodes import NodeEncoder
from inidiff import diff_structure

upload_root = "/tmp"

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = upload_root


def _diff_lines(l, r):
    return list(difflib.unified_diff(l.splitlines(), r.splitlines()))


def _diff(l, r):
    try:
        return {"type": "semantic", "result": diff_structure(l, r)}
    except:
        return {"type": "syntactic", "result": _diff_lines(l, r)}


def _save(key):
    file = request.files[key]
    filename = os.path.join(upload_root, secure_filename(file.filename))
    file.save(filename)
    return filename


@app.route("/", methods=["POST"])
def diff():
    left = _save("left_file")
    right = _save("right_file")

    with open(left) as l:
        with open(right) as r:
            res = _diff(l.read(), r.read())
            return json.dumps(res, cls=NodeEncoder)


if __name__ == "__main__":
    app.run(debug=True)
