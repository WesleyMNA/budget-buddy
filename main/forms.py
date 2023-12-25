from django import forms


class LoginForm(forms.Form):
    username = forms.CharField(label='Username', max_length=150)
    password = forms.CharField(label='Password', max_length=150)


class SingUpForm(forms.Form):
    name = forms.CharField(label='Name', max_length=150)
    username = forms.CharField(label='Username', max_length=150)
    email = forms.EmailField(label='Email', max_length=254)
    password = forms.CharField(label='Password', max_length=150)
    confirm_password = forms.CharField(label='Confirm Password', max_length=150)
