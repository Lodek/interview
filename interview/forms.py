from django import forms

from base.models import Candidate, Position
from .models import Template

class SetupForm(forms.Form):
    candidate = forms.ModelChoiceField(Candidate.objects.all())
    position = forms.ModelChoiceField(Position.objects.all())
    template = forms.ModelChoiceField(Template.objects.all())
