from file_frontend.routes.health import health


def register_blueprints(app):
    app.register_blueprint(health.health)
