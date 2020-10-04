# Intro
Repository for the interview app.

The app is a Django application with a Postgre database.

# Running
The web app is written using django, the python environment dependencies are managed by poetry and the application is run from within docker.

To run it for development use `docker-compose up` in the root directory.
The application webapplication will be available on port 8000

PS. your milleage may vary as the docker-compose expects your GID and UID to be 1000.
That was done in order to avoid running `chown` everytime `manage.py` was used to create files.

# Deploy
Work in progress right now.
Need to setup a docker-compose to run an application server and configure nginx to serve the static files, as django doesn't do that out of the box.

# About
To knowo more about the app, checkout the [about](./About.md)
