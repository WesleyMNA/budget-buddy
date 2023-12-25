from django import forms


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

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            print('ERROR')
            raise forms.ValidationError('passwords do not match')
