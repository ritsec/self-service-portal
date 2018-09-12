"""
utils.py

Author:     Sean Newman
Created:    9 September 2018
Description:
    General-use utility and helper functions.
"""
# Library imports
import smtplib

from datetime import datetime, timedelta
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from os import environ
from secrets import token_urlsafe

# External imports
from flask import (
    current_app, request
)

# Local imports
from portal.db import get_db


def check_email_code(code):
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
    try:
        sender_pass = environ['EMAIL_PASS']
    except KeyError:
        return False

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
    return True