from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate
from .models import CustomUser

# Signup Form
class CustomUserSignupForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=50, required=True)
    last_name = forms.CharField(max_length=50, required=True)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']
        labels = {
            "username": "Username",
            "email": "Email",
            "first_name": "First Name",
            "last_name": "Last Name",
            "password1": "Enter Password",
            "password2": "Enter Password Again"
        }

        error_messages = {
            'username': {
                'unique': "This username is already in use. Please choose a different one."
            },
            'email': {
                'unique': "This email is already registered. Use a different email address."
            },
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if commit:
            user.save()
        return user


# Login Form
class CustomUserLoginForm(forms.Form):
    username = forms.CharField(max_length=20, label='Username', widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter your username',
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter your password',
    }), label='Password')

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')

        if username and password:
            self.user = authenticate(self.request, username=username, password=password)
            if self.user is None:
                raise forms.ValidationError("Invalid username or password")

        return cleaned_data

    def get_user(self):
        return self.user
