from flask import Blueprint, render_template, session, redirect, request
from file_frontend.services.file_api import FileApi
import logging

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
    return send_to_google_drive()


def send_to_google_drive():
    # Authorise account with Google Drive. Once authorised, it will automatically make
    # a callback to this method because of a configured redirect rule (see readme)
    if 'credentials' not in session:
        logger.info('credentials not found in session')
        file_api_client = FileApi()
        drive_auth_json = file_api_client.authorise_drive_account()
        session['state'] = drive_auth_json['state']
        return redirect(drive_auth_json['url'])

    logger.info("User authorised")

    # TODO: add extra func
    return 'User has been authorised and credentials have been stored. More to do soon!'


@file.route('/oauth2callback')
def oauth2callback():
    # This will be the route that is called back from authorising the user with Google Drive
    file_api_client = FileApi()
    drive_credentials_json = file_api_client.retrieve_credentials(session['state'], request.url)

    # Store the credentials, so that the file can be uploaded to the correct account
    session['credentials'] = drive_credentials_json['credentials']

    # Go to send_to_google_drive function to continue process
    return send_to_google_drive()
