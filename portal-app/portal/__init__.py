"""
__init__.py

Author:     Sean Newman
Created:    28 August 2018
Description:
    All application factories used for configuring and running the application.
"""
# External imports
from flask import Flask

# Internal imports
from .config import get_config
from .database import db


def create_app():
    # Create and configure the app
    app = Flask(__name__)
    app.config.from_object(get_config())

    # Set up database
    db.init_app(app)

    # Set up blueprints
    from . import root
    app.register_blueprint(root.bp)
    app.add_url_rule('/', endpoint='index')

    from . import account
    app.register_blueprint(account.bp)

    return app
