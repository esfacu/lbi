from django import forms
from .models import LBI


class LBIForm(forms.ModelForm):
    class Meta:
        model = LBI
        fields = ['Number']