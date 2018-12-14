import flask

from src.models.stores import store


store_blueprint = flask.Blueprint(name='stores', import_name=__name__)


@store_blueprint.route('/')
def index():
    all_stores = store.Store.get_all()
    return flask.render_template('stores/index.html', all_stores=all_stores)
