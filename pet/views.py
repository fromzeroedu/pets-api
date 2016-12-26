from flask import Blueprint

from pet.api import PetAPI

pet_app = Blueprint('pet_app', __name__)

pet_app.add_url_rule('/pets/', view_func=PetAPI.as_view('pets'))
