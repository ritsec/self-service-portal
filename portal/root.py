"""
root.py

Author:     Sean Newman
Created:    28 August 2018
Description:
    General endpoints and functions that don't fall under a specific path.
"""
# Library imports
import re
import smtplib

from datetime import datetime, timedelta
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from secrets import token_urlsafe

# External imports
from flask import (
    abort, Blueprint, current_app, jsonify, render_template
)

# Local imports
from portal.db import get_db
from portal.decorators import required_args

bp = Blueprint('root', __name__)


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


def make_email_body(req_1, req_2, code, path):
    email = (
        'Hello!\n'
        'We have recieved a request to {one}.\n'
        'If you did not make this request, please contact the RITSEC '
        'administrators at ritsecclub@gmail.com\n'
        'If you did make this request, please follow the link below to '
        '{two}.\n'
        '\n'
        '{url}{path}?code={code}\n'
        '\n'
        'This request was recieved from {ip} at {time}.'.format(
            one=req_1,
            two=req_2,
            url=current_app.config['APP_URL'],
            path=path,
            code=code,
            ip=request.environ['REMOTE_ADDR'],
            time=datetime.now().isoformat()
        )
    )
    return email


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


def send_email(to_address, subject, body):
    # Get configs
    sender = current_app.config['EMAIL_ACCT']
    sender_pass = environ['EMAIL_PASS']

    # Prepare email
    msg = MIMEMultipart()
    msg['From'] = sender
    msg['To'] = to_address
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    # Send email
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(sender, sender_pass)
    text = msg.as_string()
    server.sendmail(sender, to_address, text)
    server.quit()


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
