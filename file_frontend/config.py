import os

# This file should be used only for containing environment variables, nothing else
APP_NAME = os.environ["APP_NAME"] = "file_frontend"
COMMIT = os.environ["COMMIT"] = "LOCALE"
FILE_API_URI = os.environ["FILE_API_URI"] = "http://localhost:8081"
LOG_LEVEL = os.environ["LOG_LEVEL"] = "DEBUG"
UPLOAD_FOLDER = os.environ["UPLOAD_FOLDER"] = "file_frontend/temp_uploads"
os.environ["PYTHONUNBUFFERED"] = "yes"

# When running locally, disable OAuthlib's HTTPs verification.
# When running in production *do not* leave this option enabled.
# This is used for Google Drive
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'