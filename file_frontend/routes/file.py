from flask import Blueprint, render_template, session
from file_frontend.services.file_api import FileApi
import logging

file = Blueprint('file', __name__)

API_SERVICE_NAME = 'drive'
API_VERSION = 'v2'

logger = logging.getLogger()


@file.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@file.route("/send-file", methods=["POST"])
def send_file():
    # Detect what boxes were set in the html index template. Then proceed to either Dropbox or Google Drive
    logger.info("Sending file for upload")
    # Authorise account with Google Drive. Once authorised, it will automatically make
    # a callback to this method because of a configured redirect rule (see readme)
    if 'credentials' not in session:
        file_api_client = FileApi()
        authorisation_url = file_api_client.authorise_drive_account()['authorisation_url']

