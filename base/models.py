from django.db import models

from django.contrib.auth import get_user_model

class Candidate(models.Model):

    name = models.CharField(255)
    email = models.CharField(255)


class Position(models.Model):
    CL = 'Closed'
    OP = 'Open'
    STATUS_CHOICES = [
        (CL, 'Closed'),
        (OP, 'Open'),
    ]

    name = models.CharField(255)
    description = models.CharField(1024)
    status = models.CharField(max_length=2, choices=STATUS_CHOICES,
                              default=OP)
    band = models.ForeignKey('band', on_delete=models.PROTECT)


class Band(models.Model):
    band = models.CharField(2)

    
class Subarea(models.Model):
    subarea = modeels.CharField(255)

    
class Area(models.Model):
    area = modeels.CharField(255)
