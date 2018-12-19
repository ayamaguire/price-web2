from functools import wraps
import flask


def require_login(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if 'email' not in flask.session.keys() or not flask.session['email']:
            return flask.redirect(flask.url_for('users.login_user', next=flask.request.path))
        return func(*args, **kwargs)
    return decorated_function


