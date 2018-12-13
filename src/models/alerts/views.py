import flask


alert_blueprint = flask.Blueprint(name="alerts", import_name=__name__)


@alert_blueprint.route('/')
def index():
    return flask.render_template('users/alerts.html')


@alert_blueprint.route('/new', methods=['POST'])
def create_alert():
    pass


@alert_blueprint.route('/deactivate/<string:alert_id>')
def deactivate_alert(alert_id):
    pass


@alert_blueprint.route('<string:alert_id>')
def get_alert_page(alert_id):
    pass


@alert_blueprint.route('/for_user/<string:user_id>')
def get_alerts_for_user(user_id):
    pass
