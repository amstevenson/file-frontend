from flask import Blueprint, render_template, session, redirect, request
from file_frontend.services.file_api import FileApi
import logging
import json

file = Blueprint('file', __name__)

logger = logging.getLogger()


@file.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@file.route("/send-file", methods=["POST"])
def send_file():
    # Detect what boxes were set in the html index template. Then proceed to either Dropbox or Google Drive
    logger.info("Sending file for upload")
    session.clear()
    session['directory'] = 'directory'
    session['file_path'] = 'file_path'

    # if radio button is google drive selected
    return send_google_drive()


def send_google_drive():
    # Authorise account with Google Drive. Once authorised, it will automatically make
    # a callback to this method because of a configured redirect rule (see readme)
    if 'credentials' not in session:
        logger.info('credentials not found in session')
        file_api_client = FileApi()
        drive_auth_json = file_api_client.authorise_drive_account()
        session['state'] = drive_auth_json['state']
        session['url'] = drive_auth_json['url']
        return redirect(drive_auth_json['url'])


@file.route('/oauth2callback')
def oauth2callback():
    # This will be the route that is called back from authorising the user with Google Drive
    file_api_client = FileApi()
    drive_credentials_json = file_api_client.retrieve_credentials(session['state'], session['url'])
    return drive_credentials_json
