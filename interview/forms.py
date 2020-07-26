from django import forms

from base.models import Candidate, Position
from .models import Template

class SetupForm(forms.Form):
    candidate = forms.ModelChoiceField(Candidate.objects.all())
    position = forms.ModelChoiceField(Position.objects.all())
    template = forms.ModelChoiceField(Template.objects.all())


def score_form_factory(field_names, candidate_id, position_id, template_id):
    SCORE_CHOICES = [(i, i) for i in range (6)]
    fields = {name: forms.TypedChoiceField(choices=SCORE_CHOICES, coerce=int,
                                           empty_value=None, initial=0)
              for name in field_names}
    fields['candidate'] = forms.IntegerField(initial=candidate_id, disabled=True,
                                             widget=forms.HiddenInput)
    fields['template'] = forms.IntegerField(initial=template_id, disabled=True,
                                             widget=forms.HiddenInput)
    fields['position'] = forms.IntegerField(initial=position_id, disabled=True,
                                             widget=forms.HiddenInput)
    fields['SCORE_CHOCIES'] = SCORE_CHOICES
    return type('ScoreForm', (forms.Form,), fields)
