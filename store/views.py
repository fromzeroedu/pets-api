from flask import Blueprint

from store.api import StoreAPI

store_app = Blueprint('store_app', __name__)

store_view = StoreAPI.as_view('store_api')
store_app.add_url_rule('/stores/', defaults={'store_id': None},
                 view_func=store_view, methods=['GET',])
store_app.add_url_rule('/stores/', view_func=store_view, methods=['POST',])
store_app.add_url_rule('/stores/<store_id>', view_func=store_view,
                 methods=['GET', 'PUT', 'DELETE',])
