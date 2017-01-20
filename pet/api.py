from flask.views import MethodView
from flask import jsonify, request, abort
from jsonschema import Draft4Validator
from jsonschema.exceptions import best_match
import uuid
import json
import datetime

from app.decorators import app_required
from pet.models import Pet
from pet.schema import schema
from pet.templates import pet_obj, pets_obj
from store.models import Store

class PetAPI(MethodView):

    decorators = [app_required]

    def __init__(self):
        self.PETS_PER_PAGE = 10
        if (request.method != 'GET' and request.method != 'DELETE') and not request.json:
            abort(400)

    def get(self, pet_id):
        if pet_id:
            pet = Pet.objects.filter(external_id=pet_id, live=True).first()
            if pet:
                response = {
                    "result": "ok",
                    "pet": pet_obj(pet)
                }
                return jsonify(response), 200
            else:
                return jsonify({}), 404
        else:
            # pet URL template
            pet_href = "/pets/?page=%s"

            pets = Pet.objects.filter(live=True)
            if "species" in request.args:
                pets = pets.filter(species=request.args.get('species'))
                pet_href += "&species=" + request.args.get('species')
            if "breed" in request.args:
                pets = pets.filter(breed=request.args.get('breed'))
                pet_href += "&breed=" + request.args.get('breed')

            page = int(request.args.get('page', 1))
            pets = pets.paginate(page=page, per_page=self.PETS_PER_PAGE)
            response = {
                "result": "ok",
                "links": [
                    {
                        "href": pet_href % page,
                        "rel": "self"
                    }
                ],
                "pets": pets_obj(pets)
            }
            if pets.has_prev:
                response["links"].append(
                    {
                        "href": pet_href  % (pets.prev_num),
                        "rel": "previous"
                    }
                )
            if pets.has_next:
                response["links"].append(
                    {
                        "href": pet_href % (pets.next_num),
                        "rel": "next"
                    }
                )
            return jsonify(response), 200

    def post(self):
        pet_json = request.json
        error = best_match(Draft4Validator(schema).iter_errors(pet_json))
        if error:
            return jsonify({"error": error.message}), 400

        store = Store.objects.filter(external_id=pet_json.get('store')).first()
        if not store:
            error = {
                "code": "STORE_NOT_FOUND"
            }
            return jsonify({'error': error}), 400

        try:
            received_date = datetime.datetime.strptime(
                pet_json.get('received_date'), "%Y-%m-%dT%H:%M:%SZ")
        except:
            return jsonify({"error": "INVALID_DATE"}), 400

        pet = Pet(
            external_id=str(uuid.uuid4()),
            name=pet_json.get('name'),
            species=pet_json.get('species'),
            breed=pet_json.get('breed'),
            age=pet_json.get('age'),
            store=store,
            price=pet_json.get('price'),
            received_date=received_date
        ).save()
        response = {
            "result": "ok",
            "pet": pet_obj(pet)
        }
        return jsonify(response), 201

    def put(self, pet_id):
        pet = Pet.objects.filter(external_id=pet_id, live=True).first()
        if not pet:
            return jsonify({}), 404
        pet_json = request.json
        error = best_match(Draft4Validator(schema).iter_errors(pet_json))
        if error:
            return jsonify({"error": error.message}), 400

        store = Store.objects.filter(external_id=pet_json.get('store')).first()
        if not store:
            error = {
                "code": "STORE_NOT_FOUND"
            }
            return jsonify({'error': error}), 400

        try:
            received_date = datetime.datetime.strptime(
                pet_json.get('received_date'), "%Y-%m-%dT%H:%M:%SZ")
        except:
            return jsonify({"error": "INVALID_DATE"}), 400

        pet.name = pet_json.get('name')
        pet.species = pet_json.get('species')
        pet.breed = pet_json.get('breed')
        pet.age = pet_json.get('age')
        pet.store = store
        pet.price = pet_json.get('price')
        pet.received_date = received_date
        pet.save()
        response = {
            "result": "ok",
            "pet": pet_obj(pet)
        }
        return jsonify(response), 200

    def delete(self, pet_id):
        pet = Pet.objects.filter(external_id=pet_id, live=True).first()
        if not pet:
            return jsonify({}), 404
        pet.live = False
        pet.save()
        return jsonify({}), 204
