import os

from flask import Flask


def create_app(test_config=None):
    # Create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'portal.db'),
        WEBCMD_HOST='localhost',
        WEBCMD_PORT='5000',
        WEBCMD_SCHEMA='http',
    )

    if test_config is None:
        # Load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # Load the test config if passed on
        app.config.from_mapping(test_config)

    # Ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # Set up database
    from . import db
    db.init_app(app)

    # Set up blueprints
    from . import ui
    app.register_blueprint(ui.bp)
    app.add_url_rule('/', endpoint='index')

    from . import account
    app.register_blueprint(account.bp)

    return app
