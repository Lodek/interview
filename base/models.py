from django.db import models

from django.contrib.auth import get_user_model

class Candidate(models.Model):

    name = models.CharField(255)


class Position(models.Model):
    pass


class Band(models.Model):

    band = models.CharField(2)

    
