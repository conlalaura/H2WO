from flask import Flask


def create_app():
    app = Flask(__name__)

    with app.app_context():
        # Register blueprints
        from .routes import main  # import routes

        app.register_blueprint(main)

    return app
