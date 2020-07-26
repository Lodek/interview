from django import forms

from base.models import Candidate, Position
from .models import Template

class SetupForm(forms.Form):
    candidate = forms.ModelChoiceField(Candidate.objects.all())
    position = forms.ModelChoiceField(Position.objects.all())
    template = forms.ModelChoiceField(Template.objects.all())

class ScoreForm(forms.Form):
    SCORE_CHOICES = [(i, i) for i in range (6)]
    score = forms.TypedChoiceField(choices=SCORE_CHOICES , 
                                   coerce=int, empty_value=None)

def score_form_factory(field_names):
    SCORE_CHOICES = [(i, i) for i in range (6)]
    fields = {name: forms.TypedChoiceField(choices=SCORE_CHOICES, coerce=int,
                                           empty_value=None)
              for name in field_names}
    fields['SCORE_CHOCIES'] = SCORE_CHOICES
    return type('ScoreForm', (forms.Form,), fields)
