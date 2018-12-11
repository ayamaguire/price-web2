from flask import Blueprint


items_blueprint = Blueprint(name="items", import_name=__name__)


@items_blueprint.route('/item/<string:name>')
def item_page(name):
    pass

