from file_frontend.routes import health


def register_blueprints(app):
    app.register_blueprint(health.health)
