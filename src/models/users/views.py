from flask import Blueprint, request, session, redirect, url_for, render_template

from src.models.users import constants as c
from src.models.users import user, exceptions


user_blueprint = Blueprint(name='users', import_name=__name__)


@user_blueprint.route('/login', methods=['GET', 'POST'])
def login_user():
    if request.method == 'POST':
        # Check the login
        email = request.form[c.EMAIL]
        hashed = request.form[c.HASHED]
        try:
            if user.User.user_valid(email, hashed):
                session[c.EMAIL] = email
                return redirect(url_for('.user_alerts'))
        except exceptions.UserError as e:
            return e.message
    return render_template('users/login.html')


@user_blueprint.route('/register', methods=['GET', 'POST'])
def register_user():
    if request.method == 'POST':
        # Check the login
        email = request.form[c.EMAIL]
        hashed = request.form[c.HASHED]
        try:
            if user.User.register_user(email, hashed):
                session[c.EMAIL] = email
                return redirect(url_for('.user_alerts'))
        except exceptions.UserError as e:
            return e.message
    return render_template('users/register.html')


@user_blueprint.route('/profile')
def user_profile():
    return "This is the profile page."


@user_blueprint.route('/settings')
def user_settings():
    return "This is the settings page"


@user_blueprint.route('/logout')
def logout_user():
    pass


@user_blueprint.route('/check_alerts/<string:user_id>')
def check_user_alerts(user_id):
    pass
