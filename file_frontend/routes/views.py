from flask import Blueprint, render_template

general = Blueprint('general', __name__)


@general.route("/", methods=["GET"])
def index():
    return render_template("index.html")
