"""
database.py

Author:     Sean Newman
Created:    28 August 2018
Description:
    Functions and CLI commands for interacting with the database.
"""
# Library imports
from datetime import datetime as dt
from os import environ

# External imports
import click

from flask import current_app, g
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class EmailCode(db.Model):
    value = db.Column(
        db.String(200),
        unique=True,
        nullable=False,
        primary_key=True
    )
    user = db.Column(db.Text, nullable=False)
    created = db.Column(db.DateTime, nullable=False, default=dt.utcnow)
    expires = db.Column(db.DateTime)


def init_db(app):
    with app.app_context():            
        while True:
            try:
                db.init_app(app)
            except Exception:
                pass
            else:
                break
        db.create_all()
