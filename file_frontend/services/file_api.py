from flask import current_app as app
from urllib.parse import urljoin
import logging
import json
import requests
from urllib.parse import quote

logger = logging.getLogger()


class FileApi(object):

    def __init__(self):
        self.base_url = app.config["FILE_API_URI"]

    def authorise_drive_account(self):
        logging.info("Making request to File-API to authorise Google Drive account")
        # Make a call to File-API. Note that we do not need to process the response, as Google Drive
        # Makes a redirect of its own to a specified endpoint
        _url = urljoin(self.base_url, "{0}".format("get-authorisation-url"))
        logging.debug("The request to get-authorisation-url is using url: " + _url)

        return json.loads(requests.get(_url).text)

    def retrieve_credentials(self, state, request_url):
        logging.info("Making request to File-API to retrieve Google Drive account credentials")
        quote_url = quote(request_url)

        # Make a call to File-API. Note that we do not need to process the response, as Google Drive
        # Makes a redirect of its own to a specified endpoint
        _url = self.base_url + "/get-credentials?state=" + state + "&url=" + quote_url
        logging.debug("The request to get-credentials is using url: " + _url)

        return json.loads(requests.get(_url).text)
