from flask.views import MethodView
from flask import request, abort, jsonify
import bcrypt
import uuid
from datetime import datetime, timedelta

from app.models import App, Access

class AppAPI(MethodView):

    def __init__(self):
        if not request.json:
            abort(400)

    def post(self):
        if not "app_id" in request.json or not "app_secret" in request.json:
            error = {
                "code": "MISSING_APP_ID_OR_APP_SECRET"
            }
            return jsonify({'error': error}), 400
        existing_app = App.objects.filter(app_id=request.json.get('app_id')).first()
        if existing_app:
            error = {
                "code": "APP_ID_ALREADY_EXISTS"
            }
            return jsonify({'error': error}), 400
        else:
            # create the credentials
            salt = bcrypt.gensalt()
            hashed_password = bcrypt.hashpw(request.json.get('app_secret'), salt)
            app = App(
                app_id=request.json.get('app_id'),
                app_secret=hashed_password
            ).save()
            return jsonify({'result': 'ok'})

class AccessAPI(MethodView):

    def __init__(self):
        if not request.json:
            abort(400)

    def post(self):
        if not "app_id" in request.json or not "app_secret" in request.json:
            error = {
                "code": "MISSING_APP_ID_OR_APP_SECRET"
            }
            return jsonify({'error': error}), 400

        app = App.objects.filter(app_id=request.json.get('app_id')).first()
        if not app:
            error = {
                "code": "INCORRECT_CREDENTIALS"
            }
            return jsonify({'error': error}), 403
        else:
            # generate a token
            if bcrypt.hashpw(request.json.get('app_secret'), app.app_secret) == app.app_secret:
                # delete existing tokens
                existing_tokens = Access.objects.filter(app=app).delete()
                token = str(uuid.uuid4())
                now = datetime.utcnow().replace(second=0, microsecond=0)
                expires = now + timedelta(days=30)
                access = Access(
                    app=app,
                    token=token,
                    expires=expires
                ).save()
                expires_3339 = expires.isoformat("T") + "Z"
                return jsonify({'token': token, 'expires': expires_3339}), 200
            else:
                error = {
                    "code": "INCORRECT_CREDENTIALS"
                }
                return jsonify({'error': error}), 403
