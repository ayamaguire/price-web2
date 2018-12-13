import flask


store_blueprint = flask.Blueprint(name='stores', import_name=__name__)


@store_blueprint.route('/')
def index():
    return flask.render_template('stores/list.html')


@store_blueprint.route('/<string:name>')
def store_page(name):
    return flask.render_template('stores/store.html', name=name)

