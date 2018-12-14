import flask
import flask_wtf
import wtforms

from src.models.users import constants
from src.models.users import user, exceptions
from src.common import utils


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
        password = utils.Utils.encrypt_password(flask.request.form[constants.PASSWORD])
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


@user_blueprint.route('/settings', methods=['GET', 'POST'])
def user_settings():
    email = flask.session[constants.EMAIL]
    email_form = UpdateEmailForm()
    password_form = UpdatePasswordForm()
    if not email:
        # this means the user navigated directly to this page, because we don't show this link when not logged in
        return flask.render_template('users/login.html', email_form=email_form, password_form=password_form)
    current_user = user.User.get_by_email(email)
    if flask.request.method == 'POST':
        if email_form.data and email_form.submit1.data:
            update_email = email_form.data['name']
            current_user.email = update_email
            flask.session['email'] = update_email
        if password_form.data and password_form.submit2.data:
            update_password = password_form.data['name']
            current_user.password = utils.Utils.encrypt_password(update_password)
        current_user.save_to_db()
    return flask.render_template('users/settings.html', email_form=email_form, password_form=password_form)


@user_blueprint.route('/logout')
def logout_user():
    flask.session[constants.EMAIL] = None
    return flask.redirect(flask.url_for('home_display'))


@user_blueprint.route('/check_alerts/<string:user_id>')
def check_user_alerts(user_id):
    pass


class UpdateEmailForm(flask_wtf.FlaskForm):
    name = wtforms.StringField('email', validators=[wtforms.validators.DataRequired()])
    submit1 = wtforms.SubmitField(label='submit')


class UpdatePasswordForm(flask_wtf.FlaskForm):
    name = wtforms.StringField('email', validators=[wtforms.validators.DataRequired()])
    submit2 = wtforms.SubmitField(label='submit')
