from django import forms
from django.contrib.auth.models import User

from main.models import Revenue, Expense

FORM_INPUT_CLASS = 'form-input'
RADIO_INPUT_CLASS = 'radio-input'


class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = [
            'title',
            'value',
            'date',
            'description',
            'category',
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': FORM_INPUT_CLASS}),
            'value': forms.NumberInput(attrs={'class': FORM_INPUT_CLASS}),
            'date': forms.SelectDateWidget(attrs={'class': FORM_INPUT_CLASS}),
            'description': forms.Textarea(attrs={'class': FORM_INPUT_CLASS}),
            'category': forms.RadioSelect(attrs={'class': RADIO_INPUT_CLASS}),
        }

    def save(self, user: User):
        expense = super().save(commit=False)
        expense.user = user
        expense.save()
        return expense


class LoginForm(forms.Form):
    username = forms.CharField(
        label='Username',
        max_length=150,
        widget=forms.TextInput(attrs={'class': FORM_INPUT_CLASS, 'id_for_label': 'Teste'})
    )
    password = forms.CharField(
        label='Password',
        max_length=150,
        widget=forms.PasswordInput(attrs={'class': FORM_INPUT_CLASS})
    )


class RevenueForm(forms.ModelForm):
    class Meta:
        model = Revenue
        fields = [
            'title',
            'value',
            'date',
            'description',
            'category',
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': FORM_INPUT_CLASS}),
            'value': forms.NumberInput(attrs={'class': FORM_INPUT_CLASS}),
            'date': forms.SelectDateWidget(attrs={'class': FORM_INPUT_CLASS}),
            'description': forms.Textarea(attrs={'class': FORM_INPUT_CLASS}),
            'category': forms.RadioSelect(attrs={'class': RADIO_INPUT_CLASS}),
        }

    def save(self, user: User):
        expense = super().save(commit=False)
        expense.user = user
        expense.save()
        return expense


class SingUpForm(forms.Form):
    name = forms.CharField(
        label='Name',
        max_length=150,
        widget=forms.TextInput(attrs={'class': FORM_INPUT_CLASS})
    )
    username = forms.CharField(
        label='Username',
        max_length=150,
        widget=forms.TextInput(attrs={'class': FORM_INPUT_CLASS})
    )
    email = forms.EmailField(
        label='Email',
        max_length=254,
        widget=forms.TextInput(attrs={'class': FORM_INPUT_CLASS})
    )
    password = forms.CharField(
        label='Password',
        max_length=150,
        widget=forms.PasswordInput(attrs={'class': FORM_INPUT_CLASS})
    )
    confirm_password = forms.CharField(
        label='Confirm Password',
        max_length=150,
        widget=forms.PasswordInput(attrs={'class': FORM_INPUT_CLASS})
    )

    def clean_username(self):
        username = self.cleaned_data['username']
        exists = User.objects.filter(username=username).exists()

        if exists:
            raise forms.ValidationError('username already exists')

        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        exists = User.objects.filter(email=email).exists()

        if exists:
            raise forms.ValidationError('email already exists')

        return email

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError('passwords do not match')
