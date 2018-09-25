"""
__init__.py

Author:     Sean Newman
Created:    28 August 2018
Description:
    All application factories used for configuring and running the application.
"""
# Library imports
from os import environ

# External imports
from flask import Flask

# Internal imports
from . import config


def create_app():
    # Create and configure the app.  Note that the FLASK_ENV variable is set,
    # which is noticed by Flask's Click setup.  If you run Flask with docker,
    # then there are more options.  However, the command-line initialization
    # only recognizes 'development' and 'production'.
    app = Flask(__name__)
    env = environ['FLASK_ENV']
    if env == 'development':
        app.config.from_object(config.DevelopmentConfig)
    elif env == 'production':
        app.config.from_object(config.ProductionConfig)

    # Set up database
    from . import db
    db.init_app(app)

    # Set up blueprints
    from . import root
    app.register_blueprint(root.bp)
    app.add_url_rule('/', endpoint='index')

    from . import account
    app.register_blueprint(account.bp)

    return app
