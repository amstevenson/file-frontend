from flask import Flask
# from file_frontend.logconfig import register_logging

# register_logging()
app = Flask(__name__)
app.config.from_pyfile("config.py")
