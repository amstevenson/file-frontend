# file-frontend

A micro-service that acts as a frontend for functionality revolving around uploading files to Google Drive. Both this
service and file-api need to be running in order to achieve this.

If you are going to make use of this project, you will need to follow the steps related to setting up a Google Drive Api
project (https://developers.google.com/drive/v3/web/quickstart/python). The secret file will need to be placed in the
main directory of file-api.

Refer to file-api's readme for more information about this.

## Running

### Fastest way (standalone):

python3 ./manage.py runserver

### Virtualenv

1) Virtualenv venv
2) source venv/Scripts/activate - for windows
or source venv/bin/activate - mac
3) install dependencies (can use requirements.txt for this)
4) set FLASK_APP variable with
    "set FLASK_APP=manage.py" (for windows)
    or "export FLASK_APP=manage.py" (for mac)
5) flask run

### Docker (still a work in progress)

With purely docker (go to main directory):

1) docker build -t file_frontend .
2) docker run -p 8080:80 file_frontend
