"""
root.py

Author:     Sean Newman
Created:    28 August 2018
Description:
    General endpoints that don't fall under a specific path.
"""
# Library imports
import re

# External imports
from flask import (
    abort, Blueprint, jsonify, render_template, request
)

# Local imports
from portal.decorators import required_args
from portal.utils import *

bp = Blueprint('root', __name__)


##
#   Routes
##
@bp.route('/email', methods=['POST'])
@required_args(post_args=['type', 'email'])
def email():
    # Make sure it's an RIT email
    if re.search(r'@((mail|g)\.)?rit\.edu$', request.form['email']) is None:
        return jsonify({'status': 'please use an RIT email'}), 400

    # Create new code
    code = new_code(request.form['email'])

    # Send correct email for the request type
    if request.form['type'] == 'account.register':
        send_email(
            request.form['email'],
            'RITSEC Account Registration Link',
            make_email_body(
                'create a new RITSEC account for this email address',
                'create your new RITSEC account',
                code,
                '/account/register'
            )
        )
        return jsonify({'status': 'email sent'})

    elif request.form['type'] == 'account.change-password':
        send_email(
            request.form['email'],
            'RITSEC Account Password Reset Link',
            make_email_body(
                'reset the password for the RITSEC account associated with '
                'this email address',
                'change your account\'s password',
                code,
                '/account/change-password'
            )
        )
        return jsonify({'status': 'email sent'})

    else:
        # If the type argument is not one of the above, we don't know what to
        # do with it.
        return jsonify({'status': 'unknown type provided'}), 400


@bp.route('/', methods=['GET'])
def index():
    return render_template('index.html')
