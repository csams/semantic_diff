"""
Provide an endpoint for structural diffs.

Uses custom parsers for different file types. If they fail, falls
back to line based unified diffs.
"""
import difflib
import tempfile
from contextlib import contextmanager

from flask import Flask, jsonify, request

from semdiff import differs
from semdiff.diff_ast import NodeEncoder

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = tempfile.gettempdir()
app.json_encoder = NodeEncoder


def _diff_lines(l, r):
    """
    This is the default diff used if a structural one can't be looked up or
    fails.
    """
    return list(difflib.unified_diff(l.splitlines(), r.splitlines()))


def _diff(kind, l, r):
    """
    Attempt a structural diff of `l` and `r` based on their kind. If a structural
    differ is missing or fails, fall back to a line based unified diff.
    """
    if kind is None:
        return {"type": "syntactic", "result": _diff_lines(l, r)}

    try:
        differ = differs.DIFFERS[kind]
        return {"type": "structural", "result": differ(l, r)}
    except:
        return {"type": "syntactic", "result": _diff_lines(l, r)}


@contextmanager
def _saved_file(key):
    file = request.files[key]
    with tempfile.NamedTemporaryFile(mode="r+") as tmp:
        file.save(tmp.name)
        yield tmp


@app.route("/", methods=["POST"])
def diff():
    """
    POST the two things to diff as files. Include a "kind" form parameter
    for the kind of structural diff to try.
    """
    with _saved_file("left_file") as l:
        with _saved_file("right_file") as r:
            kind = request.values.get("kind")
            res = _diff(kind, l.read(), r.read())
            return jsonify(res)
