from flask import Flask, abort

from helpers import ipfs_call

app = Flask(__name__)


@app.route("/")
def hello_world():
    return "Functions are CIDs you say???"


@app.route("/call/<fn_cid>/on/<arg_cid>")
def call(fn_cid, arg_cid):
    try:
        return {"result": ipfs_call(fn_cid, arg_cid)}
    except Exception as e:
        print(f"OOPS: {e}")
        abort(500)
