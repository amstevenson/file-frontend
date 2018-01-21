def credentials_to_dict(credentials):
    return {'token': credentials.token,
            'refresh_token': credentials.refresh_token,
            'token_uri': credentials.token_uri,
            'client_id': credentials.client_id,
            'client_secret': credentials.client_secret,
            'scopes': credentials.scopes}


def construct_upload_headers(file_type, content_length, auth_token):
        return {
                'Content-Type': file_type,
                'Content_Length': str(content_length),
                'Authorization': 'Bearer ' + auth_token
        }


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
