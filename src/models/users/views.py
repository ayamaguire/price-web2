import flask
from src.models.users import constants
from src.models.users import user, exceptions


user_blueprint = flask.Blueprint(name='users', import_name=__name__)


@user_blueprint.route('/login', methods=['GET', 'POST'])
def login_user():
    if flask.request.method == 'POST':
        # TODO: investigate if we should hash the password client side
        email = flask.request.form[constants.EMAIL]
        password = flask.request.form[constants.PASSWORD]
        try:
            if user.User.user_valid(email, password):
                flask.session[constants.EMAIL] = email
                return flask.redirect(flask.url_for('.user_profile'))
        except exceptions.UserError as e:
            return e.message
    return flask.render_template('users/login.html')


@user_blueprint.route('/register', methods=['GET', 'POST'])
def register_user():
    if flask.request.method == 'POST':
        email = flask.request.form[constants.EMAIL]
        password = flask.request.form[constants.PASSWORD]
        try:
            if user.User.register_user(email, password):
                flask.session[constants.EMAIL] = email
                return flask.redirect(flask.url_for('.user_profile'))
        except exceptions.UserError as e:
            return e.message
    return flask.render_template('users/register.html')


@user_blueprint.route('/profile')
def user_profile():
    return flask.render_template('users/alerts.html')


@user_blueprint.route('/settings')
def user_settings():
    return flask.render_template('users/settings.html')


@user_blueprint.route('/logout')
def logout_user():
    flask.session[constants.EMAIL] = None
    return flask.redirect(flask.url_for('home_display'))


@user_blueprint.route('/check_alerts/<string:user_id>')
def check_user_alerts(user_id):
    pass
