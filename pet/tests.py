from application import create_app as create_app_base
from mongoengine.connection import _get_db
import unittest
import json

from settings import MONGODB_HOST, MONGODB_DB
from pet.models import Pet
from application import fixtures

class PetTest(unittest.TestCase):

    def create_app(self):
        self.db_name = 'pets-api-test'
        return create_app_base(
            MONGODB_SETTINGS={'DB': self.db_name,
                'HOST': MONGODB_HOST},
            TESTING=True,
            WTF_CSRF_ENABLED=False,
            SECRET_KEY = 'mySecret!',
        )

    def setUp(self):
        self.app_factory = self.create_app()
        self.app = self.app_factory.test_client()

    def tearDown(self):
        db = _get_db()
        db.client.drop_database(db)

    def app_dict(self):
        return json.dumps(dict(
                app_id="pet_client",
                app_secret="pet_secret"
                ))

    def store_dict(self):
        return json.dumps(dict(
            neighborhood="Bronxville",
            street_address="1112 Bronxville Avenue",
            city="Bronx",
            state="NY",
            zip="10567",
            phone="718-222-2445"
            ))

    def pet_dict(self):
        return json.dumps(dict(
            name="Mac",
            species="Dog",
            breed="Shitzu",
            age=11,
            store=self.store_id,
            price="855.22",
            received_date="2016-11-11T12:12:01Z"
            ))

    def create_api_app(self):
        # create our app
        rv = self.app.post('/apps/',
            data=self.app_dict(),
            content_type='application/json')

    def generate_access_token(self):
        # generate an access token
        rv = self.app.post('/apps/access_token/',
            data=self.app_dict(),
            content_type='application/json')
        self.token = json.loads(rv.data.decode('utf-8')).get('token')

    def headers(self):
        return {
            'X-APP-ID': 'pet_client',
            'X-APP-TOKEN': self.token
            }

    def test_pets(self):
        # get app up and running
        self.create_api_app()
        self.generate_access_token()

        # create a store
        rv = self.app.post('/stores/',
            headers=self.headers(),
            data=self.store_dict(),
            content_type='application/json')
        self.store_id = json.loads(rv.data.decode('utf-8')).get('store')['id']
        assert rv.status_code == 201

        # Create a pet
        rv = self.app.post('/pets/',
            headers=self.headers(),
            data=self.pet_dict(),
            content_type='application/json')
        pet_id = json.loads(rv.data.decode('utf-8')).get('pet')['id']
        assert rv.status_code == 201

        # get a pet
        rv = self.app.get('/pets/' + pet_id,
            headers=self.headers(),
            content_type='application/json')
        assert rv.status_code == 200

        # edit a pet
        new_pet = json.dumps(dict(
            name="Apple",
            species="Cat",
            breed="Siamese",
            age=12,
            store=self.store_id,
            price="566.22",
            received_date="2016-12-11T12:12:01Z"
            ))
        rv = self.app.put('/pets/' + pet_id,
            headers=self.headers(),
            data=new_pet,
            content_type='application/json')
        assert rv.status_code == 200
        assert json.loads(rv.data.decode('utf-8')).get('pet')['species'] == "Cat"

        # delete a pet
        rv = self.app.delete('/pets/' + pet_id,
            headers=self.headers(),
            content_type='application/json')
        assert rv.status_code == 204
        assert Pet.objects.filter(live=False).count() == 1

    def test_pagination(self):
        # get app up and running
        self.create_api_app()
        self.generate_access_token()

        # import fixtures
        fixtures(self.db_name, "store", "store/fixtures/stores.json")
        fixtures(self.db_name, "pet", "pet/fixtures/pets.json")

        # get all pets
        rv = self.app.get('/pets/',
            headers=self.headers(),
            content_type='application/json')
        assert "next" in str(rv.data)

        # get second page of pets
        rv = self.app.get('/pets/?page=2',
            headers=self.headers(),
            content_type='application/json')
        assert "previous" in str(rv.data)
