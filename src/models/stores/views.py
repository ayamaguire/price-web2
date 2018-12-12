from flask import Blueprint


store_blueprint = Blueprint(name='stores', import_name=__name__)


@store_blueprint.route('/')
def index():
    return "This is the stores index"


@store_blueprint.route('/stores/<string:name>')
def store_page(name):
    pass

