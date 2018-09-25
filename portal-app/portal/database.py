"""
database.py

Author:     Sean Newman
Created:    28 August 2018
Description:
    Functions and CLI commands for interacting with the database.
"""
# Library imports
from datetime.datetime import utcnow

# External imports
import click

from flask import current_app, g
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class EmailCode(db.Model):
    value = db.Column(db.Text, unique=True, nullable=False, primary_key=True)
    user = db.Column(db.Text, nullable=False)
    created = db.Column(db.DateTime, nullable=False, server_default=utcnow)
    expires = db.Column(db.DateTime)
