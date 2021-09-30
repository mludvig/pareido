import os

from flask import Flask


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)

    from . import models
    models.load_models()

    from . import main
    app.register_blueprint(main.bp)

    return app
