import flask
import flask_wtf
import wtforms

from src.models.alerts import constants
from src.models.alerts import alert
from src.models.items import item
from src.models.stores import exceptions as StoreExceptions


alert_blueprint = flask.Blueprint(name="alerts", import_name=__name__)


@alert_blueprint.route('/')
def index():
    user_alerts = alert.Alert.get_by_email(flask.session['email'])
    return flask.render_template('alerts/index.html', alerts=user_alerts)


@alert_blueprint.route('/create', methods=['GET', 'POST'])
def create_alert():
    if flask.request.method == "POST":
        item_name = flask.request.form[constants.ITEM_NAME]
        url = flask.request.form[constants.ITEM_URL]
        desired_price = flask.request.form[constants.DESIRED_PRICE]
        try:
            new_item = item.Item(name=item_name, url=url)
            new_item.save_to_db()
            new_alert = alert.Alert(user_email=flask.session['email'], item_id=new_item._id, price_limit=desired_price)
            new_alert.update_price()
            user_alerts = alert.Alert.get_by_email(flask.session['email'])
            return flask.render_template('alerts/index.html', alerts=user_alerts)
        except StoreExceptions.StoreNotFoundError:
            return flask.render_template('stores/create.html', url=url)

    return flask.render_template('alerts/create.html')


@alert_blueprint.route('/remove/<string:alert_id>')
def remove_alert(alert_id):
    to_delete = alert.Alert.get_by_id(_id=alert_id)
    to_delete.remove()
    return flask.redirect(flask.url_for('alerts.index'))


# TODO: implement alert deactivation. For now, they can just delete and re make.
# @alert_blueprint.route('/deactivate/<string:alert_id>')
# def deactivate_alert(alert_id):
#     pass


@alert_blueprint.route('/edit/<string:alert_id>', methods=['GET', 'POST'])
def edit_alert(alert_id):
    email = flask.session['email']
    if not email:
        return flask.render_template('users/login.html')
    current_alert = alert.Alert.get_by_id(_id=alert_id)
    name_form = UpdateNameForm()
    url_form = UpdateUrlForm()
    price_form = UpdatePriceForm()
    if flask.request.method == "POST":
        if name_form.data and name_form.submit1.data:
            current_alert.item.name = name_form.data['name']
            current_alert.item.save_to_db()
        if url_form.data and url_form.submit2.data:
            current_alert.url = url_form.data['name']
            current_alert.item.save_to_db()
        if price_form.data and price_form.submit3.data:
            current_alert.price_limit = price_form.data['name']
            current_alert.save_to_db()
        return flask.redirect(flask.url_for('alerts.index'))
    return flask.render_template('alerts/edit.html',
                                 alert=current_alert,
                                 name_form=name_form,
                                 url_form=url_form,
                                 price_form=price_form)


@alert_blueprint.route('<string:alert_id>')
def get_alert_page(alert_id):
    pass


@alert_blueprint.route('/for_user/<string:user_id>')
def get_alerts_for_user(user_id):
    pass


class UpdateNameForm(flask_wtf.FlaskForm):
    name = wtforms.StringField('item_name', validators=[wtforms.validators.DataRequired()])
    submit1 = wtforms.SubmitField(label='submit')


class UpdateUrlForm(flask_wtf.FlaskForm):
    name = wtforms.StringField('item_url', validators=[wtforms.validators.DataRequired()])
    submit2 = wtforms.SubmitField(label='submit')


class UpdatePriceForm(flask_wtf.FlaskForm):
    name = wtforms.StringField('item_price', validators=[wtforms.validators.DataRequired()])
    submit3 = wtforms.SubmitField(label='submit')
