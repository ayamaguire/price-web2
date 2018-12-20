import flask

from src.common import database
from src.models.users.views import user_blueprint
from src.models.stores.views import store_blueprint
from src.models.alerts.views import alert_blueprint


app = flask.Flask(__name__)
app.secret_key = "EZEXkgbj8hTKfFa5D3jrQxwh69fqkJQT"


@app.before_first_request
def initialize_db():
    database.Database.initialize()


@app.route('/')
def home_display():
    return flask.render_template('home.html')


app.register_blueprint(user_blueprint, url_prefix='/users')
app.register_blueprint(store_blueprint, url_prefix='/stores')
app.register_blueprint(alert_blueprint, url_prefix='/alerts')
