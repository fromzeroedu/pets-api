from flask.views import MethodView
from flask import jsonify, request, abort

class PetAPI(MethodView):

    pets = [
        { "id": 1, "name": u"Mac" },
        { "id": 2, "name": u"Leo" },
        { "id": 3, "name": u"Brownie" }
    ]

    def get(self):
        return jsonify({"pets": self.pets})

    def post(self):
        if not request.json or not 'name' in request.json:
            abort(400)
        pet = {
            "id": len(self.pets) + 1,
            "name": request.json["name"]
        }
        self.pets.append(pet)
        return jsonify({'pet': pet}), 201
