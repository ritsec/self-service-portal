"""
decorators.py

Author:     Sean Newman
Created:    6 September 2018
Description:
    Function decorators that can be used across the application to perform
    certain functions in a standard way.
"""
# Library imports
import functools

# External imports
from flask import abort


class required_args(object):
    """
    Checks all requests on the decorated route for the specified arguments.
    If a request does not contain all required arguments, a 400 error is
    returned.
    """
    def __init__(self, post_args=None, get_args=None):
        self.post_args = post_args
        self.get_args = get_args

    def __call__(self, route):
        @functools.wraps(route)
        def wrapped_route(*args, **kwargs):
            if request.method == 'GET' and isinstance(self.get_args, list):
                for key in self.get_args:
                    if key not in request.args:
                        abort(400)

            elif request.method == 'POST' and isinstance(self.post_args, list):
                for key in self.post_args:
                    if key not in request.form:
                        abort(400)

            return route(*args, **kwargs)
        return wrapped_route


class requires_code(object):
    """
    Checks the email code for all requests on the decorated route for validity.
    If the code is not valid, a 403 error is returned.

    This decorator should be used after (under) the "required_args" decorator.
    """
    def __init__(self, methods):
        self.methods = methods

    def __call__(self, route):
        @functools.wraps(route)
        def wrapped_route(*args, **kwargs):
            if request.method in self.methods:
                if not check_code(request.values['code']):
                    abort(403)

            return route(*args, **kwargs)
        return wrapped_route
