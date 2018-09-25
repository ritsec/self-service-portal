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
import requests

from flask import current_app, request

# Local imports
from portal.database import db, EmailCode


def check_email_code(code):
    # Check if code is in database
    entry = EmailCode.query.filter_by(value=code).first()
    if entry is None:
        return False

    expiration = entry.expires

    # Make sure code is not expired
    if expiration < datetime.now():
        return False

    return entry.user


def delete_code(code):
    db.session.delete(EmailCode.query.filter_by(value=code).first())
    db.session.commit()


def get_user_id(email):
    """Get the GitLab user ID for a user, specified by email"""
    resp = requests.get('{url}/users?search={email}'.format(
        url=current_app.config['GITLAB_URL'],
        email=email,
    ), headers={'Private-Token': token=environ['GITLAB_API_TOKEN']})
    # TODO: document gitlab api token env var

    # Make sure we only got one response
    if len(resp.json()) > 1:
        return None
    else:
        return resp.json()[0]['id']


def make_bad_email_body(req_1, req_2):
    email = (
        'Hello!\n'
        'We have recieved a request to {one}.\n'
        'If you did not make this request, you may ignore this email for '
        'now.  If you continue to get these emails, please contact the RITSEC '
        'administrators at ritsecclub@gmail.com\n'
        'If you did make this request, {two}.\n'
        '\n'
        'This request was recieved from {ip} at {time}.'.format(
            one=req_1,
            two=req_2,
            ip=request.environ['REMOTE_ADDR'],
            time=datetime.now().isoformat(),
        )
    )


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
    # Generate securely random 32-byte base64 encoded url-safe string.  We
    # assume there will be no duplicates of these.
    code = token_urlsafe(64)

    # Get timestamp of 4 hours from now
    # TODO: update documentation
    expiry = datetime.now() + timedelta(hours=4)

    # Add code to database
    db.session.add(EmailCode(value=code, user=user, expires=expiry))
    db.session.commit()
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
