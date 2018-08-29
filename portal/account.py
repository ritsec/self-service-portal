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
                    if key not in request.values:
                        abort(400)

            elif request.method == 'POST' and isinstance(self.post_args, list):
                for key in self.post_args:
                    if key not in request.values:
                        abort(400)

            return route(*args, **kwargs)
        return wrapped_route


class requires_code(object):
    """
    Checks the email code for all requests on the decorated route for validity.
    If the code is not valid, a 403 error is returned.

    This decorator should be used after (under) the "required_args" decorator.
    """
    def __init__(self, methods):
        self.methods = methods

    def __call__(self, route):
        @functools.wraps(route)
        def wrapped_route(*args, **kwargs):
            if request.method in self.methods:
                if not check_code(request.values['code']):
                    abort(403)

            return route(*args, **kwargs)
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


def uncached_response(resp):
    # Add headers to tell everyone not to cache this response
    resp.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    resp.headers['Pragma'] = 'no-cache'
    resp.headers['Expires'] = '0'
    return resp


##
#   Routes
##
@bp.route('/change-password', methods=['GET', 'POST'])
@required_args(post_args=['code', 'user', 'password'], get_args=['code'])
@requires_code(methods=['POST', 'GET'])
def change_password():
    # Handle form submission
    if request.method == 'POST':
        # Send password change request
        resp = requests.post('{schema}://{host}:{port}/change-password'.format(
            schema=current_app.config['WEBCMD_SCHEMA'],
            host=current_app.config['WEBCMD_HOST'],
            port=current_app.config['WEBCMD_PORT'],
        ), data={
            'username': request.values['user'],
            'new_password': request.values['password'],
        })
        if resp.status_code == 200:
            db = get_db()
            db.execute(
                'DELETE FROM EMAIL_CODE WHERE code = ?',
                (request.values['code'], )
            )
            db.commit()
            return redirect(url_for('account.success'))
        else:
            return redirect(url_for('account.error'))

    # Serve UI
    resp = make_response(render_template(
        'account/change-password.html', user=check_code(request.values['code'])
    ))
    return uncached_response(resp)


@bp.route('/error', methods=['GET'])
def error():
    return render_template('account/error.html')


@bp.route('/generate-code', methods=['GET'])
@required_args(get_args=['user'])
def generate_code():
    # TODO email code instead of posting code
    # TODO create UI for submitting email for code
    return new_code(request.values['user'])


@bp.route('/register', methods=['GET', 'POST'])
@required_args(post_args=['code', 'fname', 'lname', 'email', 'password'])
@requires_code(['GET', 'POST'])
def create():
    # Handle form submission
    if request.method == 'POST':
        # Send user creation request
        resp = requests.post('{schema}://{host}:{port}'.format(
            schema=current_app.config['WEBCMD_SCHEMA'],
            host=current_app.config['WEBCMD_HOST'],
            port=current_app.config['WEBCMD_PORT'],
        ), data={
            'fname': request.values['fname'],
            'lname': request.values['lname'],
            'email': request.values['email'],
        })

        if resp.status_code == 200:
            delete_code(request.values['code'])
            return redirect(url_for('account.success'))
        else:
            return redirect(url_for('account.error'))

    # Serve UI
    resp = make_response(render_template(
        'account/register.html', user=check_code(request.values['code'])
    ))
    return uncached_response(resp)


@bp.route('/success', methods=['GET'])
def change_successful():
    return render_template('account/success.html')
