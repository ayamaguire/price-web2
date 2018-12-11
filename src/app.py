import flask

from src.common import database
from src.models.users.views import user_blueprint


database.Database.initialize()


app = flask.Flask(__name__)
app.config.from_object('config')
app.secret_key = "EZEXkgbj8hTKfFa5D3jrQxwh69fqkJQT"


@app.route('/')
def home_display():
    return flask.render_template('home.html')


app.register_blueprint(user_blueprint, url_prefix='/users')
