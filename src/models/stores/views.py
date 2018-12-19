import flask
import flask_wtf
import wtforms

from src.models.users import decorators as user_decorators
from src.models.stores import store
from src.models.stores import constants
from src.models.stores import exceptions as StoreExceptions


store_blueprint = flask.Blueprint(name='stores', import_name=__name__)


@store_blueprint.route('/')
def index():
    all_stores = store.Store.get_all()
    return flask.render_template('stores/index.html', all_stores=all_stores)


@store_blueprint.route('/edit/<string:store_id>', methods=['GET', 'POST'])
@user_decorators.requires_login
def edit_store(store_id):
    current_store = store.Store.get_by_id(_id=store_id)
    name_form = UpdateStoreNameForm()
    url_form = UpdateStoreUrlForm()
    tag_form = UpdateTagNameForm()
    query_object_form = UpdateQueryObjectForm()
    query_value_form = UpdateQueryValueForm()
    current_key = list(current_store.query.keys())[0]
    current_value = current_store.query.get(current_key)
    if flask.request.method == "POST":
        if name_form.data and name_form.submit1.data:
            current_store.name = name_form.data['name']
        if url_form.data and url_form.submit2.data:
            current_store.domain = url_form.data['name']
        if tag_form.data and tag_form.submit3.data:
            current_store.tag_name = tag_form.data['name']
        if query_object_form.data and query_object_form.submit4.data:
            query_object_form.query = {tag_form.data['name']: current_value}
        if query_value_form.data and query_value_form.submit5.data:
            query_object_form.query = {current_key: tag_form.data['name']}
        current_store.save_to_db()
        return flask.redirect(flask.url_for('stores.index'))
    return flask.render_template('stores/edit.html',
                                 store_id=store_id,
                                 store=current_store,
                                 key=current_key,
                                 value=current_value,
                                 forms=[name_form, url_form, tag_form, query_object_form, query_value_form])


@store_blueprint.route('/remove/<string:store_id>')
@user_decorators.requires_login
def remove_store(store_id):
    return "Remove the store with id {}".format(store_id)


@store_blueprint.route('/create', methods=['GET', 'POST'])
@user_decorators.requires_login
def create_store():
    if flask.request.method == "POST":
        store_name = flask.request.form[constants.STORE_NAME]
        url = flask.request.form[constants.STORE_URL]
        tag_name = flask.request.form[constants.TAG_NAME]
        query_object = flask.request.form[constants.QUERY_OBJECT]
        query_value = flask.request.form[constants.QUERY_VALUE]
        try:
            store.Store.get_by_url(url)
            return "The desired store already exists!"
        except StoreExceptions.StoreNotFoundError:
            new_store = store.Store(name=store_name, domain=url, tag_name=tag_name, query={query_object: query_value})
            new_store.save_to_db()
            return flask.redirect(flask.url_for('stores.index'))

    return flask.render_template('stores/create.html')


class UpdateStoreNameForm(flask_wtf.FlaskForm):
    name = wtforms.StringField(constants.STORE_NAME, validators=[wtforms.validators.DataRequired()])
    submit1 = wtforms.SubmitField(label='submit')


class UpdateStoreUrlForm(flask_wtf.FlaskForm):
    name = wtforms.StringField(constants.STORE_URL, validators=[wtforms.validators.DataRequired()])
    submit2 = wtforms.SubmitField(label='submit')


class UpdateTagNameForm(flask_wtf.FlaskForm):
    name = wtforms.StringField(constants.TAG_NAME, validators=[wtforms.validators.DataRequired()])
    submit3 = wtforms.SubmitField(label='submit')


class UpdateQueryObjectForm(flask_wtf.FlaskForm):
    name = wtforms.StringField(constants.QUERY_OBJECT, validators=[wtforms.validators.DataRequired()])
    submit4 = wtforms.SubmitField(label='submit')


class UpdateQueryValueForm(flask_wtf.FlaskForm):
    name = wtforms.StringField(constants.QUERY_VALUE, validators=[wtforms.validators.DataRequired()])
    submit5 = wtforms.SubmitField(label='submit')
