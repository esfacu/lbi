from django import forms
from .models import LBI, Ean

class LBIForm(forms.ModelForm):
    class Meta:
        model = LBI
        fields = ['Number']

class LBISelectionForm(forms.Form):
    lbi_choices = [(lbi.id, str(lbi)) for lbi in LBI.objects.all()]
    selected_lbi = forms.ChoiceField(choices=lbi_choices, widget=forms.RadioSelect)

class EanCreationForm(forms.ModelForm):
    class Meta:
        model = Ean
        fields = ['ean_code']