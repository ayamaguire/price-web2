from functools import wraps
import flask
import os


def requires_login(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if 'email' not in flask.session.keys() or not flask.session['email']:
            return flask.redirect(flask.url_for('users.login_user', next=flask.request.path))
        return func(*args, **kwargs)
    return decorated_function


def requires_admin(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if 'email' not in flask.session.keys() or not flask.session['email']:
            return flask.redirect(flask.url_for('users.login_user', next=flask.request.path))
        if flask.session['email'] != os.environ.get('ADMIN'):
            return flask.redirect(flask.url_for('users.admin_required'))
        return func(*args, **kwargs)
    return decorated_function
