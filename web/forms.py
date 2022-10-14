from django import forms
from django.contrib.auth.models import User

from .models import Car


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username', 'password']



class CompareForm(forms.Form):

    car1 = forms.ModelChoiceField(
        Car.objects.all(),
        required=True,
        widget=forms.Select(
            attrs={'class': 'selectpicker', 'data-live-search': "true"}
        )
    )
    car2 = forms.ModelChoiceField(
        Car.objects.all(),
        required=True,
        widget=forms.Select(
            attrs={'class': 'selectpicker', 'data-live-search': "true"}
        )
    )

class Orden(forms.Form):
    nombre = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    address = forms.CharField(label='direccion',widget=forms.TextInput(attrs={'class': 'form-control'}))
    identificacion = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))

