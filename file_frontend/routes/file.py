from flask import Blueprint, render_template, session, redirect, request
from file_frontend.services.file_api import FileApi
from file_frontend.utils.fileutils import read_file
from werkzeug import secure_filename
import logging
import os

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

    # Retrieve the POST information
    uploaded_file = request.files['file']
    file_name = secure_filename(uploaded_file.filename)
    destination = request.form.get('destination')

    if not destination or not file_name:
        return "Please enter a destination and select a file"

    file_type = uploaded_file.content_type

    logger.debug("(Before authentication) Sending to Google Drive with destination of: {} , file name of: {} , "
                 "file_type of: {} ".format(destination, file_name, file_type))

    # Save file locally so that it can be opened. This is in order to retrieve the bytes that are required
    # when making a request to Google Drive APIs
    file_path = os.path.join(UPLOAD_FOLDER, file_name)
    uploaded_file.save(file_path)

    return authorise_and_upload(file_name, file_path, file_type, destination)


def authorise_and_upload(file_name, file_path, file_type, destination):
    # Authorise account with Google Drive. Once authorised, it will automatically make
    # a callback to this method because of a configured redirect rule (see readme)
    if 'token' not in session:
        logger.info('credentials not found in session')
        file_api_client = FileApi()
        authorisation_response = file_api_client.get_authorisation_details()

        # Save session values. These should be in a database. This is so they can be used on the
        # response back from Google Drive.
        session['state'] = authorisation_response['state']
        session['file_name'] = file_name
        session['file_path'] = file_path
        session['file_type'] = file_type
        session['destination'] = destination

        return redirect(authorisation_response['url'])

    logger.info("User authorised")
    return upload_file(file_name, file_path, file_type, destination)


def upload_file(file_name, file_path, file_type, destination):

    # Open the file in order to retrieve the byte information.
    file_data = read_file(file_path)

    file_length = len(file_data)
    logger.debug("Size of returned data is {}".format(file_length))

    # Remove the temporary file that was saved at the start of the process
    os.remove(file_path)

    # Upload the metadata to include the name of the file
    # file_id = response['id']
    # response = file_api_client.modify_file_metadata(file_name, file_type, session['token'], file_id)
    # logging.debug("Response from Google Drive modify metadata is: {}".format(response))

    # Upload metadata and retrieve the resumeable upload location
    file_api_client = FileApi()
    response_location = file_api_client.upload_file_metadata(file_name, file_type, session['token'], file_length)
    logging.debug("Response location from Google Drive metadata upload is: {}".format(response_location))

    # Upload the file
    response = file_api_client.upload_file(file_length, file_type, session['token'], file_data, response_location)
    logging.debug("Response from Google Drive upload is: {}".format(response))

    # TODO: create a redirect page for this. Simple as.
    return 'File has been uploaded successfully'


@file.route('/oauth2callback')
def oauth2callback():
    # This will be the route that is called back from authorising the user with Google Drive
    logger.info("Response detected from Google Drive. User has been authorised.")
    file_api_client = FileApi()
    drive_credentials_json = file_api_client.get_credentials(session['state'], request.url)

    # Store the credentials, so that the file can be uploaded to the correct account
    session['token'] = drive_credentials_json['credentials']['token']

    # Go to send_to_google_drive function to continue process
    return authorise_and_upload(session['file_name'], session['file_path'],
                                session['file_type'], session['destination'])
