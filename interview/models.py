from django.db import models

from django.contrib.auth import get_user_model

class Question(models.Model):

    question = models.CharField(max_length=500)

    answer = models.CharField(max_length=500)

    band = models.ForeignKey('base.Band', on_delete=models.PROTECT,
                             related_name='questions')

    subarea = models.ForeignKey('base.Subarea', on_delete=models.SET_NULL,
                                null=True, related_name='questions')


class Template(models.Model):

    owner = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL,
                              null=True, related_name='templates')

    name = models.CharField(max_length=255)

    description = models.CharField(max_length=500)


class Interview(models.Model):

    date = models.DateTimeField(auto_now=True)

    interviewer = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL,
                                    null=True, related_name='interviews' )

    position = models.ForeignKey('base.Position', on_delete=models.SET_NULL,
                                 null=True, related_name='interviews')

    candidate = models.ForeignKey('base.Candidate', on_delete=models.SET_NULL,
                                  null=True, related_name='interviews')


class Score(models.Model):

    question = models.ForeignKey('Question', on_delete=models.PROTECT,
                                 related_name='scores')

    interview = models.ForeignKey('Interview', on_delete=models.PROTECT,
                                 related_name='scores')

    score = models.IntegerField()
