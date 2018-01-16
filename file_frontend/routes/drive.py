from flask import Blueprint, redirect, session, url_for, jsonify, request
from file_frontend.utils.driveutils import credentials_to_dict
import os

import google_auth_oauthlib.flow

drive = Blueprint('drive', __name__)

SCOPES = ['https://www.googleapis.com/auth/drive']

# The client secret file is downloaded from the created project from the drive apis
DRIVE_CLIENT_SECRETS_FILE = os.getenv("CLIENT_SECRETS_FILE")
DRIVE_APP_SECRET_KEY = os.getenv("DRIVE_APP_SECRET_KEY")


@drive.route('/authorise')
def authorise():
    # Create flow instance to manage the OAuth 2.0 Authorization Grant Flow steps.
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        DRIVE_CLIENT_SECRETS_FILE, scopes=SCOPES)

    flow.redirect_uri = url_for('drive.oauth2callback', _external=True)

    authorization_url, state = flow.authorization_url(
        # Enable offline access so that you can refresh an access token without
        # re-prompting the user for permission. Recommended for web server apps.
        access_type='offline',
        # Enable incremental authorization. Recommended as a best practice.
        include_granted_scopes='true')

    # Store the state so the callback can verify the auth server response.
    session['state'] = state

    return redirect(authorization_url)


@drive.route('/oauth2callback')
def oauth2callback():
    # Specify the state when creating the flow in the callback so that it can
    # verified in the authorization server response.
    state = session['state']

    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        DRIVE_CLIENT_SECRETS_FILE, scopes=SCOPES, state=state)
    flow.redirect_uri = url_for('drive.oauth2callback', _external=True)

    # Use the authorization server's response to fetch the OAuth 2.0 tokens.
    authorization_response = request.url
    flow.fetch_token(authorization_response=authorization_response)

    # Store credentials in the session.
    # TODO: In a production version, id likely want to save these
    #              credentials in a persistent database instead.
    credentials = flow.credentials
    #session['credentials'] = credentials_to_dict(credentials)

    return url_for('drive.oauth2callback', _external=True)
