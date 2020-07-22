from django.db import models


class Question(models.Model):

    question = models.CharField(500)
    answer = models.CharField(500)

    band = models.ForeignKey()
    subarea = models.ForeignKey()


class Template(models.Model):

    owner = 
    name = 
    description = 


class Interview(models.Model):

    date = 
    interviewer = 
    position = 
    candidate = 
    scores =

    
class Score(models.Model):

    question = 
    interview = 
    score = 
