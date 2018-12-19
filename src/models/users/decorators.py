from functools import wraps
import flask

# TODO: figure out how to access the config without causing circular import
# from src.app import app


def requires_login(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if 'email' not in flask.session.keys() or not flask.session['email']:
            return flask.redirect(flask.url_for('users.login_user', next=flask.request.path))
        return func(*args, **kwargs)
    return decorated_function


# def requires_admin(func):
#     @wraps(func)
#     def decorated_function(*args, **kwargs):
#         if 'email' not in flask.session.keys() or not flask.session['email']:
#             return flask.redirect(flask.url_for('users.login_user', next=flask.request.path))
#         if flask.session['email'] not in app.config['ADMINS']:
#             return flask.redirect(flask.url_for('users.login_user'))
#         return func(*args, **kwargs)
#     return decorated_function
