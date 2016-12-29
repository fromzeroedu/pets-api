from flask.views import MethodView
from flask import jsonify, request, abort, render_template
import uuid
import json
from jsonschema import Draft4Validator
from jsonschema.exceptions import best_match

from app.decorators import app_required
from store.models import Store
from store.schema import schema
from store.templates import store_obj, stores_obj

class StoreAPI(MethodView):

    decorators = [app_required]

    def __init__(self):
        if request.method != 'GET' and not request.json:
            abort(400)

    def get(self, store_id):
        if store_id:
            store = Store.objects.filter(external_id=store_id).first()
            if store:
                response = {
                    "result": "ok",
                    "store": store_obj(store)
                }
                return jsonify(response), 200
            else:
                return jsonify({}), 404
        else:
            stores = Store.objects.all()
            response = {
                "result": "ok",
                "stores": stores_obj(stores)
            }
            return jsonify(response), 200

    def post(self):
        store_json = request.json
        error = best_match(Draft4Validator(schema).iter_errors(store_json))
        if error:
            return jsonify({"error": error.message}), 400
        else:
            store = Store(
                external_id=str(uuid.uuid4()),
                neighborhood=store_json.get('neighborhood'),
                street_address=store_json.get('street_address'),
                city=store_json.get('city'),
                state=store_json.get('state'),
                zip=store_json.get('zip'),
                phone=store_json.get('phone')
            ).save()
            response = {
                "result": "ok",
                "store": store_obj(store)
            }
            return jsonify(response), 201

    def put(self, pet_id):
        pass

    def delete(self, pet_id):
        pass
