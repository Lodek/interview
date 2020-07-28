#!/bin/sh
docker-compose --file Devops/docker-compose-prod.yml --project-directory . exec web python manage.py createsuperuser
