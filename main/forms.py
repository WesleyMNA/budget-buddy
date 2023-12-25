from django import forms
from django.contrib.auth.models import User


class LoginForm(forms.Form):
    username = forms.CharField(
        label='Username',
        max_length=150
    )
    password = forms.CharField(
        label='Password',
        max_length=150,
        widget=forms.PasswordInput()
    )


class SingUpForm(forms.Form):
    name = forms.CharField(
        label='Name',
        max_length=150
    )
    username = forms.CharField(
        label='Username',
        max_length=150
    )
    email = forms.EmailField(
        label='Email',
        max_length=254
    )
    password = forms.CharField(
        label='Password',
        max_length=150,
        widget=forms.PasswordInput()
    )
    confirm_password = forms.CharField(
        label='Confirm Password',
        max_length=150,
        widget=forms.PasswordInput()
    )

    def clean_username(self):
        username = self.cleaned_data['username']
        exists = User.objects.filter(username=username).exists()

        if exists:
            raise forms.ValidationError('username already exists')

    def clean_email(self):
        email = self.cleaned_data['email']
        exists = User.objects.filter(email=email).exists()

        if exists:
            raise forms.ValidationError('email already exists')

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError('passwords do not match')
