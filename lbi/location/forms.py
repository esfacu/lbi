from django import forms
from .models import LBI, Ean, CustomUser
from django.core.validators import RegexValidator
from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

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
        
class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(
        max_length=8,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Cédula de identidad'})
    )
    password = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'})
    )

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')

        if username and password:
            user = authenticate(username=username, password=password)

            if user is None:
                raise forms.ValidationError(
                    self.error_messages['invalid_login'],
                    code='invalid_login',
                    params={'username': self.username_field.verbose_name},
                )

        return cleaned_data

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'Nombre', 'Tienda', 'email')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            