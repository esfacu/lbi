from django import forms
from .models import LBI, Ean

class LBIForm(forms.ModelForm):
    class Meta:
        model = LBI
        fields = ['Number']

class LBISelectionForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(LBISelectionForm, self).__init__(*args, **kwargs)
        lbi_choices = [(lbi.id, str(lbi)) for lbi in LBI.objects.all()]
        self.fields['selected_lbi'] = forms.ChoiceField(choices=lbi_choices, widget=forms.Select)

class EanCreationForm(forms.ModelForm):
    class Meta:
        model = Ean
        fields = ['ean_code']