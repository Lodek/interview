from django import forms

def select_form_factory(field_names):
    CHOICES = (False, True)
    fields = {name: forms.TypedChoiceField(choices=CHOICES, coerce=bool,
                                           required=False, initial=False,
                                           widget=forms.CheckboxInput, )
              for name in field_names}
    fields['CHOCIES'] = CHOICES
    return type('ScoreForm', (forms.Form,), fields)

class ListFilterForm(forms.Form):
    candidate = forms.CharField(required=False)
