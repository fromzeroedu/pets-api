from flask import Blueprint

home_app = Blueprint('home_app', __name__)

@home_app.route('/')
def home():
    return "Hello World!"
