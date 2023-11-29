from django import forms
from .models import LBI, Ean
from django.core.validators import RegexValidator

class LBIForm(forms.ModelForm):
    # Define un RegexValidator para el formato nnn-nn-nnn
    lbi_format_validator = RegexValidator(
        regex=r'^\d{3}-\d{2}-\d{3}$',
        message='El formato del LBI debe ser nnn-nn-nnn.',
        code='invalid_format'
    )

    # Aplica el validator al campo Number
    Number = forms.CharField(
        max_length=10,
        validators=[lbi_format_validator],
        widget=forms.TextInput(attrs={'placeholder': 'Ingrese Rack nnn-nn-nnn'})
    )

    class Meta:
        model = LBI
        fields = ['Number']

class LBISelectionForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(LBISelectionForm, self).__init__(*args, **kwargs)
        self.fields['selected_lbi'] = forms.CharField(max_length=10, widget=forms.TextInput(attrs={'placeholder': 'Ingrese Rack'}))

class EanCreationForm(forms.ModelForm):
    class Meta:
        model = Ean
        fields = ['ean_code']