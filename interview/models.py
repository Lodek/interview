from django.db import models

from django.contrib.auth import get_user_model

from viz.stats import StatCalculator

import json

class Question(models.Model):

    question = models.CharField(max_length=500)

    answer = models.CharField(max_length=5000)

    seniority = models.ForeignKey('base.Seniority', on_delete=models.PROTECT,
                             related_name='questions')

    subarea = models.ForeignKey('base.Subarea', on_delete=models.SET_NULL,
                                null=True, related_name='questions')

    weight = models.IntegerField()

    def as_dict(self):
        attrs = 'question answer seniority subarea weight'.split()
        dict = {attr: str(getattr(self, attr)) for attr in attrs}
        dict['weight'] = int(dict['weight'])
        return dict

    def __str__(self):
        return self.question


class Template(models.Model):

    owner = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL,
                              null=True, related_name='templates')

    name = models.CharField(max_length=255)

    description = models.CharField(max_length=500)

    questions = models.ManyToManyField('Question', related_name='+')

    def __str__(self):
        return self.name


class Interview(models.Model):

    date = models.DateTimeField(auto_now=True)

    interviewer = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL,
                                    null=True, related_name='interviews' )

    position = models.ForeignKey('base.Position', on_delete=models.SET_NULL,
                                 null=True, related_name='interviews')

    candidate = models.ForeignKey('base.Candidate', on_delete=models.SET_NULL,
                                  null=True, related_name='interviews')

    comments = models.CharField(max_length=5000)

    @property
    def question_scores(self):
        return {score.question: score.score for score in self.scores.all()}

    @property
    def result(self):
        return StatCalculator().calculate_avg([(score.question, score.score)
                                               for score in self.scores.all()])
    def as_dict(self):
        calc = StatCalculator()
        flat_attrs = 'date interviewer position candidate comments'.split()
        scores = self.question_scores
        stringfy = lambda d: {str(key): value for key, value in d.items()}
        dict = {attr: str(getattr(self, attr)) for attr in flat_attrs}
        dict['area_results'] = stringfy(calc.calculate_area_avg(scores))
        dict['subarea_results'] = stringfy(calc.calculate_subarea_avg(scores))
        dict['seniority_results'] = stringfy(calc.calculate_seniority_avg(scores))

        scores = []
        for question, score in self.question_scores.items():
            d = question.as_dict()    
            d.pop('answer')
            d['score'] = score
            scores.append(d)
        dict['scores'] = score
        return dict

    def jsonfy(self):
        return json.dumps(self.as_dict(), indent=4)


class Score(models.Model):

    question = models.ForeignKey('Question', on_delete=models.PROTECT,
                                 related_name='scores')

    interview = models.ForeignKey('Interview', on_delete=models.PROTECT,
                                 related_name='scores')

    score = models.IntegerField()
