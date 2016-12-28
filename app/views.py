from flask import Blueprint

from app.api import AppAPI, AccessAPI

app_app = Blueprint('app_app', __name__)

app_view = AppAPI.as_view('app_api')
app_app.add_url_rule('/apps/', view_func=app_view, methods=['POST',])

access_view = AccessAPI.as_view('access_api')
app_app.add_url_rule('/apps/access_token/', view_func=access_view, methods=['POST',])
