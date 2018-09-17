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
    # TODO: add form to index page
    # Handle form submission
    if request.method == 'POST':
        # Send password change request
        resp = requests.post('{url}/change-password'.format(
            url=current_app.config['WEBCMD_URL'],
        ), data={
            'email': g.user,
            'new_password': request.form['password'],
        })
        if resp.status_code == 200:
            db = get_db()
            db.execute(
                'DELETE FROM EMAIL_CODE WHERE code = ?',
                (request.form['code'], )
            )
            db.commit()
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
    post_args=['code', 'fname', 'lname', 'password'],
    get_args=['code']
)
@requires_code(['GET', 'POST'])
def register():
    # TODO: add to index page
    # Handle form submission
    if request.method == 'POST':
        # Send user creation request
        resp = requests.post('{url}/register'.format(
            url=current_app.config['WEBCMD_URL']
        ), data={
            'fname': request.form['fname'],
            'lname': request.form['lname'],
            'email': g.user,
            'password': request.form['password']
        })

        if resp.status_code == 200:
            delete_code(request.form['code'])
            return jsonify({'status': 'success'}), 200
        else:
            return jsonify({
                'status': 'failure occurred at user creation agent'
            }), 500

    # Serve registration form
    return render_template(
        'account/register.html',
        username=g.user,
        email_code=request.args['code']
    )
