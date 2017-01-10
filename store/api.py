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
from pet.models import Pet
from pet.templates import pets_obj

class StoreAPI(MethodView):

    decorators = [app_required]

    def __init__(self):
        self.STORES_PER_PAGE = 10
        self.PETS_PER_PAGE = 10
        if (request.method != 'GET' and request.method != 'DELETE') and not request.json:
            abort(400)

    def get(self, store_id):
        if store_id:
            store = Store.objects.filter(external_id=store_id, live=True).first()
            if store:
                if "pets" in request.url:
                    pets = Pet.objects.filter(store=store, live=True)
                    page = int(request.args.get('page', 1))
                    pets = pets.paginate(page=page, per_page=self.PETS_PER_PAGE)
                    response = {
                        "result": "ok",
                        "links": [
                            {
                                "href": "/stores/%s/pets/?page=%s" % (store_id, page),
                                "rel": "self"
                            }
                        ],
                        "store": store_obj(store),
                        "pets": pets_obj(pets, nostore=True)
                    }
                    if pets.has_prev:
                        response["links"].append(
                            {
                                "href": "/stores/%s/pets/?page=%s" % (store_id, pets.prev_num),
                                "rel": "previous"
                            }
                        )
                    if pets.has_next:
                        response["links"].append(
                            {
                                "href": "/stores/%s/pets/?page=%s" % (store_id, pets.next_num),
                                "rel": "next"
                            }
                        )
                else:
                    response = {
                        "result": "ok",
                        "store": store_obj(store)
                    }
                return jsonify(response), 200
            else:
                return jsonify({}), 404
        else:
            stores = Store.objects.filter(live=True)
            page = int(request.args.get('page', 1))
            stores = stores.paginate(page=page, per_page=self.STORES_PER_PAGE)
            response = {
                "result": "ok",
                "links": [
                    {
                        "href": "/stores/?page=%s" % page,
                        "rel": "self"
                    }
                ],
                "stores": stores_obj(stores)
            }
            if stores.has_prev:
                response["links"].append(
                    {
                        "href": "/stores/?page=%s" % (stores.prev_num),
                        "rel": "previous"
                    }
                )
            if stores.has_next:
                response["links"].append(
                    {
                        "href": "/stores/?page=%s" % (stores.next_num),
                        "rel": "next"
                    }
                )
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

    def put(self, store_id):
        store = Store.objects.filter(external_id=store_id, live=True).first()
        if not store:
            return jsonify({}), 404
        store_json = request.json
        error = best_match(Draft4Validator(schema).iter_errors(store_json))
        if error:
            return jsonify({"error": error.message}), 400
        else:
            store.neighborhood = store_json.get('neighborhood')
            store.street_address = store_json.get('street_address')
            store.city = store_json.get('city')
            store.state = store_json.get('state')
            store.zip = store_json.get('zip')
            store.phone = store_json.get('phone')
            store.save()
            response = {
                "result": "ok",
                "store": store_obj(store)
            }
            return jsonify(response), 200

    def delete(self, store_id):
        store = Store.objects.filter(external_id=store_id, live=True).first()
        if not store:
            return jsonify({}), 404
        store.live = False
        store.save()
        return jsonify({}), 204
