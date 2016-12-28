from application import db

class App(db.Document):
    app_id = db.StringField(db_field="ai", unique=True)
    app_secret = db.StringField(db_field="as")

    meta = {
        'indexes': [('app_id')]
    }

class Access(db.Document):
    app = db.ReferenceField(App, db_field="a")
    token = db.StringField(db_field="t")
    expires = db.DateTimeField(db_field="e")
