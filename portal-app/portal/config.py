"""
config.py

Author:     Sean Newman
Created:    24 September 2018
Description:
    Configuration file that stores both dev and prod configurations.
"""
# Library imports
from os import environ, path

# External imports
from flask import current_app


def attempt_get_env(name):
    """This exists so we can declare the use of environment variables (see the
    ProductionConfig below) without Flask throwing KeyErrors left and right
    in development."""
    try:
        variable = environ[name]
    except KeyError:
        variable = ''
    finally:
        return variable


class Config():
    SECRET_KEY = ''
    SQLALCHEMY_DATABASE_URI = ''  # Used by sqlalchemy to create the engine
    APP_URL = ''  # Used to create email code links
    GITLAB_URL = ''  # Used to make GitLab API requests
    EMAIL_ACCT = 'ritsecclub@gmail.com'
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(Config):
    SECRET_KEY = 'dev'
    SQLALCHEMY_DATABASE_URI = 'sqlite://'  # In-memory SQLite database
    APP_URL = 'http://localhost:5000'
    GITLAB_URL = 'http://localhost:5000'


class ProductionConfig(Config):
    # TODO: add environment vars to master config file
    SECRET_KEY = attempt_get_env('PORTAL_SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = 'mysql://{user}:{password}@{host}/{db}'.format(
        user=attempt_get_env('SQL_USERNAME'),
        password=attempt_get_env('SQL_PASSWORD'),
        host=attempt_get_env('SQL_HOST'),
        db=attempt_get_env('SQL_DB_NAME'),
    )
    APP_URL = attempt_get_env('FRONTEND_URL')
    GITLAB_URL = attempt_get_env('GITLAB_URL')


def get_config():
    """Simple helper function to automatically grab the right config object"""
    # FLASK_ENV-to-config-class mapper dictionary
    envs = {
        'development': DevelopmentConfig,
        'production': ProductionConfig,
    }
    return envs[environ['FLASK_ENV']]
