from flask import current_app as app
from urllib.parse import urljoin
import logging
import json
import requests
from urllib.parse import quote
from file_frontend.utils.driveutils import construct_upload_headers, construct_metadata_headers, \
    construct_metadata_payload

logger = logging.getLogger()


class FileApi(object):

    def __init__(self):
        self.base_url = app.config["FILE_API_URI"]

    def get_authorisation_details(self):
        logging.info("Making request to File-API to authorise Google Drive account")
        # Make a call to File-API. Note that we do not need to process the response, as Google Drive
        # Makes a redirect of its own to a specified endpoint
        _url = urljoin(self.base_url, "{0}".format("get-authorisation-url"))
        logging.debug("The request to get-authorisation-url is using url: {}".format(_url))

        return json.loads(requests.get(_url).text)

    def get_credentials(self, state, request_url):
        logging.info("Making request to File-API to retrieve Google Drive account credentials")
        quote_url = quote(request_url)

        # Make a call to File-API. Note that we do not need to process the response, as Google Drive
        # Makes a redirect of its own to a specified endpoint
        _url = self.base_url + "/get-credentials?state=" + state + "&url=" + quote_url
        logging.debug("The request to get-credentials is using url: {}".format(_url))

        return json.loads(requests.get(_url).text)

    def upload_file(self, content_length, file_type, auth_token, file_data):
        logging.info("Making request to Google Drive API's post endpoint")
        headers = construct_upload_headers(file_type, content_length, auth_token)

        _url = 'https://www.googleapis.com/upload/drive/v3/files?uploadType=multipart'
        logging.debug("The request to upload_file is using url: {}".format(_url))

        return json.loads(requests.post(_url, data=file_data, headers=headers).text)

    def modify_file_metadata(self, file_name, file_type, auth_token, file_id):
        logging.info("Making request to Google Drive API's post endpoint to create a destination folder")
        headers = construct_metadata_headers(file_type, auth_token)
        payload = construct_metadata_payload(file_name, file_id)

        _url = urljoin("https://www.googleapis.com/drive/v3/files/", "{0}".format(file_id))
        logging.debug("The request to modify_file_metadata is using url: {}".format(_url))

        return json.loads(requests.patch(_url, data=payload, headers=headers).text)

    def create_destination_folder(self, file_name, file_type, auth_token, id):
        logging.info("Making request to Google Drive API's post endpoint to modify metadata")


