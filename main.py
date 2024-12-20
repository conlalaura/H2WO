from flask import Flask
from routes import main


def create_app():
    flask_app = Flask(__name__)
    with flask_app.app_context():
        # Register blueprints
        flask_app.register_blueprint(main)
    return flask_app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
