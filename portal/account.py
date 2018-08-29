"""
account.py

Author:     Sean Newman
Created:    28 August 2018
Description:
    Endpoints and functions that relate to account management.  All endpoints
    fall under the /account path.
"""
# Library imports
import functools

from datetime import datetime, timedelta
from secrets import token_urlsafe

# External imports
import requests

from flask import (
    abort, Blueprint, current_app, make_response, redirect, render_template,
    request, url_for
)

# Local imports
from portal.db import get_db

bp = Blueprint('account', __name__, url_prefix='/account')


##
#   Routes
##
@bp.route('/change-password', methods=['GET', 'POST'])
def change_password():
    # Handle form submission
    if request.method == 'POST':
        # Make sure there's a valid request
        if (
            'code' not in request.args or
            'user' not in request.args or
            'password' not in request.args
        ):
            abort(400)

        # Make sure the code is valid
        if not check_code('code') == request.args['user']:
            abort(403)

        # Send password change request
        resp = requests.post('{schema}://{host}:{port}/change-password'.format(
            schema=current_app.config['WEBCMD_SCHEMA'],
            host=current_app.config['WEBCMD_HOST'],
            port=current_app.config['WEBCMD_PORT'],
        ), data={
            'username': request.args['user'],
            'new_password': request.args['password'],
        })
        if resp.status_code == 200:
            db = get_db()
            db.execute(
                'DELETE FROM EMAIL_CODE WHERE code = ?',
                (request.args['code'], )
            )
            db.commit()
            return redirect(url_for('account.change_successful'))
        else:
            return redirect(url_for('account.change_unsuccessful'))

    # Serve UI
    try:
        code = request.args['c']
    except KeyError:
        # Need to send the code
        abort(400)

    user = check_code(code)
    if user is not None:
        resp = make_response(render_template(
            'account/change-password.html', user=user
        ))

        # Make sure the browser doesn't cache the page
        resp.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        resp.headers['Pragma'] = 'no-cache'
        resp.headers['Expires'] = '0'
        return resp
    else:
        abort(403)


@bp.route('/change-successful', methods=['GET'])
def change_successful():
    return render_template('account/change-successful.html')


@bp.route('/change-unsuccessful', methods=['GET'])
def change_unsuccessful():
    return render_template('account/change-unsuccessful.html')


@bp.route('/generate-code', methods=['GET'])
def generate_code():
    # TODO email code instead of posting code
    # TODO create UI for submitting email for code
    return new_code(request.args['user'])


@bp.route('/register', methods=['GET', 'POST'])
def create():
    # Handle form submission
    if request.method == 'POST':
        # Make sure there's a valid request
        if (
            'fname' not in request.args or
            'lname' not in request.args or
            'email' not in request.args or
            'code' not in request.args
        ):
            abort(400)

        # Send user creation request
        resp = requests.post('{schema}://{host}:{port}'.format(
            schema=current_app.config['WEBCMD_SCHEMA'],
            host=current_app.config['WEBCMD_HOST'],
            port=current_app.config['WEBCMD_PORT'],
        ), data={
            'fname': request.args['fname'],
            'lname': request.args['lname'],
            'email': request.args['email'],
        })

        if resp.status_code == 200:
            delete_code(request.args['code'])
            return redirect(url_for('account.change-successful.html'))
        else:
            return redirect(url_for('account.change-unsuccessful.html'))

    # Serve UI


##
#   Decorators
##
class required_args(object):
    """
    Checks all requests on the decorated route for the specified arguments.
    If a request does not contain all required arguments, a 400 error is
    returned.
    """
    def __init__(self, post_args=None, get_args=None):
        self.post_args = post_args
        self.get_args = get_args

    def __call__(self, route):
        @functools.wraps(route)
        def wrapped_route(*args, **kwargs):
            if request.method == 'GET' and isinstance(self.get_args, list):
                for key in self.get_args:
                    if key not in request.args:
                        abort(400)

            elif request.method == 'POST' and isinstance(self.port_args, list):
                for key in self.post_args:
                    if key not in request.args:
                        abort(400)

            route(*args, **kwargs)
        return wrapped_route


class requires_code(object):
    """
    Checks the email code for all requests on the decorated route for validity.
    If the code is not valid, a 403 error is returned.

    This decorator should be used after (under) the "required_args" decorator.
    """
    def __init__(self, methods=['POST']):
        self.methods = methods

    def __call__(self, route):
        @functools.wraps(route)
        def wrapped_route(*args, **kwargs):
            if request.method in self.methods:
                if not check_code(request.args['code']):
                    abort(403)

            route(args, kwargs)
        return wrapped_route


##
#   Helper functions
##
def check_code(code):
    db = get_db()

    # Check if code is in database
    entry = db.execute(
        'SELECT * FROM EMAIL_CODE WHERE val = ?', (code, )
    ).fetchone()
    if entry is None:
        return False

    expiration = datetime.fromtimestamp(int(entry['expires']))

    # Make sure code is not expired
    if expiration < datetime.now():
        return False

    return entry['user']


def delete_code(code):
    db = get_db()
    db.execute('DELTE FROM EMAIL_CODE WHERE val = ?', (code, ))
    db.commit()


def new_code(user):
    # Generate securely random 32-byte base64 encoded url-safe string
    code = token_urlsafe(32)

    # Get timestamp of tomorrow
    tomorrow = datetime.now() + timedelta(days=1)
    tomorrow = tomorrow.timestamp()

    # Add code to database
    db = get_db()
    db.execute(
        'INSERT INTO EMAIL_CODE (val, user, expires) VALUES (?, ?, ?)',
        (code, user, tomorrow)
    )
    db.commit()
    return code


##
#   Other stuff
##

# Test route to make sure valid codes return valid
# @bp.route('/hello')
# def hello():
#     code = new_code()
#     return str(check_code(code))
