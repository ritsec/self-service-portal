"""
account.py

Author:     Sean Newman
Created:    28 August 2018
Description:
    Endpoints and functions that relate to account management.  All endpoints
    fall under the /account path.
"""
# Library imports
from os import environ

# External imports
import requests

from flask import (
    abort, Blueprint, current_app, make_response, redirect, request, url_for
)

# Internal imports
from portal.decorators import required_args, requires_code

bp = Blueprint('account', __name__, url_prefix='/account')


##
#   Helper functions
##
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
    # TODO: add form to index page
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


@bp.route('/register', methods=['GET', 'POST'])
@required_args(post_args=['code', 'fname', 'lname', 'email', 'password'])
@requires_code(['GET', 'POST'])
def register():
    # TODO: add to index page
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
