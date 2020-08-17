from django import forms

from base.models import Candidate, Position
from .models import Template


class SetupForm(forms.Form):
    candidate = forms.CharField()
    position = forms.ModelChoiceField(Position.objects.all())
    template = forms.ModelChoiceField(Template.objects.all())


class ObservationsForm(forms.Form):
    SCORE_CHOICES = [(i, i) for i in range(6)]
    comments = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control'}))
    interviewer_score = forms.TypedChoiceField(choices=SCORE_CHOICES, coerce=int,
                                               empty_value=None, initial=0)

def score_form_factory(field_names):
    SCORE_CHOICES = [(i, i) for i in range(6)]
    fields = {name: forms.TypedChoiceField(choices=SCORE_CHOICES, coerce=int,
                                           empty_value=None, initial=0)
              for name in field_names}
    fields['SCORE_CHOCIES'] = SCORE_CHOICES
    return type('ScoreForm', (forms.Form,), fields)


class TemplateForm(forms.Form):
    name = forms.CharField()
    description = forms.CharField()
    csv = forms.FileField()
