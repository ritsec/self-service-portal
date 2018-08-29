from datetime import datetime, timedelta
from secrets import token_urlsafe

from flask import (
    abort, Blueprint, make_response, redirect, render_template, request,
    url_for
)

from portal.db import get_db

bp = Blueprint('account', __name__, url_prefix='/account')


##
#   Routes
##
@bp.route('/change-password', methods=['GET', 'POST'])
def change_password():
    # Do password changing
    if request.method == 'POST':
        # Send password change request
        return redirect(url_for('account.change_successful'))

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


@bp.route('/generate-code', methods=['GET'])
def generate_code():
    return new_code(request.args['user'])


@bp.route('/register', methods=['POST'])
def create():
    # TODO
    pass


##
#   Helper functions
##
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

##
#   Other stuff
##

# Test route to make sure valid codes return valid
# @bp.route('/hello')
# def hello():
#     code = new_code()
#     return str(check_code(code))
