# file-frontend

A micro-service that acts as a frontend for functionality revolving around uploading files to file hosting
providers.

The main reason this is here however is to allow me to integrate it with docker on a virtual machine. More practice
than anything else.

Haven't put too many hours into this so far, but hopefully will add the functionality

## Running

Can use a virtualenv, although there isn't much here for now. Quickest way is to use python ./manage.py runserver.

### Virtualenv

1) Virtualenv venv
2) source venv/Scripts/activate - for windows
or source venv/bin/activate - mac
3) install dependencies (can use requirements.txt for this)
4) set FLASK_APP variable with
    "set FLASK_APP=manage.py" (for windows)
    or "export FLASK_APP=manage.py" (for mac)
5) flask run