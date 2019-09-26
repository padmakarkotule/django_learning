from django import forms
from django.contrib.admin import widgets


class UserForm(forms.Form):
    username = forms.CharField(required=True, max_length=25)
    password = forms.CharField(widget=forms.PasswordInput(), required=True)
    email = forms.EmailField(required=False)

class LogoutForm(forms.Form):
    username = forms.CharField(required=True, max_length=25)


class UserCreationForm(forms.Form):
    username = forms.CharField(required=True, max_length=10)
    password = forms.CharField(widget=forms.PasswordInput(), required=True)
    email = forms.EmailField(required=False)


class CheckPermissionForm(forms.Form):
    username = forms.CharField(required=True, max_length=25)
    password = forms.CharField(widget=forms.PasswordInput(), required=True)
    email = forms.EmailField(required=False)
    service_name = forms.CharField(required=True, max_length=25)