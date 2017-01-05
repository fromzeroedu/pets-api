from flask import Blueprint

from pet.api import PetAPI

pet_app = Blueprint('pet_app', __name__)

pet_view = PetAPI.as_view('pet_api')
pet_app.add_url_rule('/pets/', defaults={'pet_id': None},
                 view_func=pet_view, methods=['GET',])
pet_app.add_url_rule('/pets/', view_func=pet_view, methods=['POST',])
pet_app.add_url_rule('/pets/<pet_id>', view_func=pet_view,
                 methods=['GET', 'PUT', 'DELETE',])
