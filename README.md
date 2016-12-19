# Running the application

- Checkout code on /opt/pets-api on local computer
- Build the containers: `docker-compose build`
- Copy settings.py.bak to settings.py and add 'mongodb' as MONGODB_HOST
- Start mongodb separately: `docker-compose up -d db`
- Start the app: `docker-compose up web`
- To start the application with pdb enabled: `docker-compose run --service-ports web`

# To access mongodb
- Find the docker web container name and run: `docker exec -it petsapi_db_1 mongo`

# To run tests
- Find the docker web container name and run: `docker exec -it petsapi_web_1 python tests.py`
