from django.db import models

from django.contrib.auth import get_user_model

class Candidate(models.Model):

    name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)


class Position(models.Model):
    OPEN = 'OP'
    CLOSED = 'CL'

    STATUS_CHOICES = [
        (CLOSED, 'Closed'),
        (OPEN, 'Open'),
    ]

    name = models.CharField(max_length=255)
    description = models.CharField(max_length=1024)
    status = models.CharField(max_length=2, choices=STATUS_CHOICES, default=OPEN)
    band = models.ForeignKey('band', on_delete=models.PROTECT)


class Band(models.Model):
    band = models.CharField(max_length=2)

    
class Subarea(models.Model):
    subarea = models.CharField(max_length=255)
    area = models.ForeignKey('area', on_delete=models.SET_NULL, null=True)

    
class Area(models.Model):
    area = models.CharField(max_length=255)
