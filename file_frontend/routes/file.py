from flask import Blueprint, render_template, session, redirect, request
from file_frontend.services.file_api import FileApi
import logging
import os
from werkzeug import secure_filename

file = Blueprint('file', __name__)

logger = logging.getLogger()
UPLOAD_FOLDER = os.getenv("UPLOAD_FOLDER")


@file.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@file.route("/send-file", methods=["POST"])
def send_file():
    # Detect what boxes were set in the html index template.
    logger.info("Sending file for upload")
    session.clear()

    # logger.info(request.files['file'])
    # f = request.files['file']
    # logger.info(f.filename)
    # f.save(secure_filename(f.filename))
    # os.remove(f)

    # Retrieve the file
    uploaded_file = request.files['file']
    filename = secure_filename(uploaded_file.filename)

    # Add values to session so that they can be used later - need to add these to a persistent database
    destination = session['destination'] = request.form.get('destination')
    session['filename'] = filename

    if not destination or not filename:
        return "Please enter a destination and select a file"

    logger.debug("(Before authentication) Sending to Google Drive with destination of: {} and file of: {}"
                 .format(destination, filename))

    # logger.debug("OS PATH: {}".format(os.path.dirname(os.path.abspath(file_name))))

    uploaded_file.save(UPLOAD_FOLDER, filename)
    # uploaded_file.save(secure_filename(uploaded_file.filename))
    remove_path = UPLOAD_FOLDER + '/' + filename
    os.removedirs(filename)

    # file_bytes = open(file_name)

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
