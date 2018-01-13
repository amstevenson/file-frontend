from file_frontend.routes import health, views


def register_blueprints(app):
    app.register_blueprint(health.health)
    app.register_blueprint(views.general)
