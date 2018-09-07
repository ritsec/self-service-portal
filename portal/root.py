"""
root.py

Author:     Sean Newman
Created:    28 August 2018
Description:
    General endpoints and functions that don't fall under a specific path.
"""
# Library imports
import smtplib

from datetime import datetime, timedelta
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from secrets import token_urlsafe

# External imports
from flask import (
    Blueprint, render_template
)

# Local imports
from portal.db import get_db

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
@bp.route('/', methods=['GET'])
def index():
    return render_template('index.html')
