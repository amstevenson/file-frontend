import json


def credentials_to_dict(credentials):
    return {'token': credentials.token,
            'refresh_token': credentials.refresh_token,
            'token_uri': credentials.token_uri,
            'client_id': credentials.client_id,
            'client_secret': credentials.client_secret,
            'scopes': credentials.scopes}


def construct_upload_headers(content_length, auth_token):
        return {
                'Content-Type': "multipart/related; boundary=foo_bar_baz",
                'Content_Length': str(content_length),
                'Authorization': 'Bearer ' + auth_token
        }


def construct_upload_body(file_name, file_type, file_data):

        file_name_json = json.dumps({'name': file_name})

        # return "--foo_bar_baz\r\nContent-Type: application/json; charset=UTF-8" \
        #        "\r\n\r\n\n" + file_name_json + "\r\n--foo_bar_baz\r\nContent-Type: " + "text/plain" + \
        #                                    "\r\n\r\n" + "A string thing" + "\r\n--foo_bar_baz--"

        return "--foo_bar_baz\r\nContent-Type: application/json; charset=UTF-8" \
               "\r\n\r\n\n" + file_name_json + "\r\n--foo_bar_baz\r\nContent-Type: " + file_type + \
               "\r\n\r\n" + str(file_data) + "\r\n--foo_bar_baz--"


def construct_metadata_headers(file_type, auth_token):
        return {
                'Content-Type': file_type,
                'Authorization': 'Bearer ' + auth_token
        }


def construct_metadata_payload(title, file_id):
        return {
                'title': title,
                'parentsCollection': [{
                        'id': file_id
                }],
                'mimeType': 'application/json'
        }
