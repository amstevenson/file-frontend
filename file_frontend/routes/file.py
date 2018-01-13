from flask import Blueprint, render_template

file = Blueprint('file', __name__)


@file.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@file.route("/send-file", methods=["POST"])
def send_file():
    return 'sent...sort of. Well, this is just a default string response.'
