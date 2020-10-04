from django import forms

from base.models import Candidate, Position
from .models import Template


#Should use ModelForm for some of these.

class SetupForm(forms.Form):
    """
    Form class for the initial setup form of the interview
    """
    candidate = forms.CharField()
    position = forms.ModelChoiceField(Position.objects.all())
    template = forms.ModelChoiceField(Template.objects.all())


class ObservationsForm(forms.Form):
    """Form for the observations screen"""
    SCORE_CHOICES = [(i, i) for i in range(6)]
    comments = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control'}))
    interviewer_score = forms.TypedChoiceField(choices=SCORE_CHOICES, coerce=int,
                                               empty_value=None, initial=0)


def score_form_factory(field_names):
    """
    Return a new class with ChoiceField for name in field_names.
    Used to generate the score checkbox for the technical interview.
    """
    SCORE_CHOICES = [(i, i) for i in range(6)]
    fields = {name: forms.TypedChoiceField(choices=SCORE_CHOICES, coerce=int,
                                           empty_value=None, initial=0)
              for name in field_names}
    fields['SCORE_CHOCIES'] = SCORE_CHOICES
    return type('ScoreForm', (forms.Form,), fields)


def skip_form_factory(field_names):
    """
    Return a new class with BooleanFiels for name in field_names.
    Used to generate the "skip" checkboxes during the interview.
    """
    fields = {name: forms.BooleanField(required=False, initial=False)
              for name in field_names}
    return type('SkipForm', (forms.Form,), fields)


class TemplateForm(forms.Form):
    """
    Form for used for uploading csv screen.
    """
    name = forms.CharField()
    description = forms.CharField()
    csv = forms.FileField()
