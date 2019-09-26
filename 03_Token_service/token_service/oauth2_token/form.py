from django import forms
from django.contrib.admin import widgets

class UserForm(forms.Form):
    username = forms.CharField(required=True, max_length=10)
    group = forms.CharField(required=True, max_length=25)
    email = forms.EmailField(required=False)