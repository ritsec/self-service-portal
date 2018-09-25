"""
account.py

Author:     Sean Newman
Created:    28 August 2018
Description:
    Endpoints and functions that relate to account management.  All endpoints
    fall under the /account path.
"""
# External imports
import requests

from flask import (
    abort, Blueprint, current_app, g, jsonify, make_response, redirect,
    render_template, request, url_for
)

# Internal imports
from portal.decorators import required_args, requires_code
from portal.utils import delete_code, get_user_id

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
@required_args(post_args=['code', 'password'], get_args=['code'])
@requires_code(methods=['POST', 'GET'])
def change_password():
    # Handle form submission
    if request.method == 'POST':
        # Remove the code
        delete_code(requests.form['code'])

        # Get user ID
        user_id = get_user_id(g.user)

        # Send password change request
        resp = requests.put('{url}/users/{id}'.format(
            url=current_app.config[''],
            id=user_id,
        ), json={
            'email': g.user,
            'password': request.form['password'],
        })
        if resp.status_code == 200:
            return jsonify({'status': 'success'}), 200
        else:
            return jsonify({
                'status': 'failure occurred at user creation agent'
            }), 500

    # Serve password reset form
    return render_template(
        'account/change-password.html',
        username=g.user,
        email_code=request.args['code']
    )


@bp.route('/register', methods=['GET', 'POST'])
@required_args(
    post_args=['code', 'username', 'fname', 'lname', 'password'],
    get_args=['code']
)
@requires_code(['GET', 'POST'])
def register():
    # Handle form submission
    if request.method == 'POST':
        # Delete the code
        delete_code(request.form['code'])

        # Send user creation request
        resp = requests.post('{url}/users'.format(
            url=current_app.config['GITLAB_URL']
        ), json={
            'email': g.user,
            'password': request.form['password'],
            'username': request.form['username'],
            'name': f'{request.form["fname"].title()} {request.form["lname"]}',
        })

        if resp.status_code == 201:
            return jsonify({'status': 'success'}), 201
        else:
            return jsonify({
                'status': 'failed to create user'
            }), 500

    # Serve registration form
    return render_template(
        'account/register.html',
        username=g.user,
        email_code=request.args['code']
    )
