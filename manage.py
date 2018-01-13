from flask_script import Manager
from file_frontend import app
import os

manager = Manager(app)


@manager.command
def runserver(port=5000):
    """Run the app using flask server"""
    os.environ["APP_NAME"] = "file-frontend"
    os.environ["COMMIT"] = "LOCAL"
    os.environ["FILE_API_URI"] = "To add"

    app.run(debug=True, port=int(port))


if __name__ == "__main__":
    manager.run()
