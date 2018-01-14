from flask import Blueprint, render_template, redirect, url_for, session, jsonify
from file_frontend.routes.drive import credentials_to_dict
import google.oauth2.credentials
import googleapiclient.discovery

file = Blueprint('file', __name__)

API_SERVICE_NAME = 'drive'
API_VERSION = 'v2'


@file.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@file.route("/send-file", methods=["POST"])
def send_file():
    # Detect what boxes were set in the html index template. Then proceed to either Dropbox or Google Drive
    return redirect(url_for('file.drive_request'))


@file.route("/drive-request")
def drive_request():
    if 'credentials' not in session:
        return redirect('drive.authorise')

    # Load credentials from the session.
    credentials = google.oauth2.credentials.Credentials(
        **session['credentials'])

    drive = googleapiclient.discovery.build(
        API_SERVICE_NAME, API_VERSION, credentials=credentials)

    files = drive.files().list().execute()

    # Save credentials back to session in case access token was refreshed.
    # TODO: In a production app, id likely want to save these
    #              credentials in a persistent database instead.
    session['credentials'] = credentials_to_dict(credentials)

    return jsonify(**files)
