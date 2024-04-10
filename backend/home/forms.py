from django import forms

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class SignupForm(UserCreationForm):
    email = forms.EmailField(max_length=200, label='Email', help_text='Required', widget=forms.TextInput(
        attrs={'placeholder': 'Email', 'class': 'input'}))
    first_name = forms.CharField(max_length=200, label='', help_text='Required', widget=forms.TextInput(
        attrs={'placeholder': 'First name', 'class': 'input'}))
    last_name = forms.CharField(max_length=200, label='', help_text='Required', widget=forms.TextInput(
        attrs={'placeholder': 'Last name', 'class': 'input'}))
    password1 = forms.CharField(max_length=200, label='', help_text='Required', widget=forms.TextInput(
        attrs={'placeholder': 'Password', 'type': 'password', 'class': 'input', 'id': 'myInput'}))
    check69 = forms.BooleanField(label='Show Password', widget=forms.CheckboxInput(
        attrs={'onclick': 'myFunction()'}))
    password2 = forms.CharField(max_length=200, label='', help_text='Required', widget=forms.TextInput(
        attrs={'placeholder': 'Confirm password', 'type': 'password', 'class': 'input'}))
    username = forms.CharField(max_length=200, label='', help_text='Required', widget=forms.TextInput(
        attrs={'placeholder': 'Username', 'class': 'input'}))

    photo = forms.ImageField(label='Profile Photo',  # Setting a label for the field
                             help_text='Please upload a profile photo',  # Providing some help text
                             required=False,  # Making the field optional
                             # Using a ClearableFileInput widget with specific attributes
                             widget=forms.ClearableFileInput(
                                 attrs={'accept': 'image/*'}),
                             error_messages={'invalid': 'Please upload a valid image file.'})  # Customizing error message for invalid files)

    # gender = forms.ChoiceField(choices=(("Male","Male"),("Female", "Female")), widget=forms.RadioSelect(attrs={"label":"Gender"}))
    # gender = forms.ChoiceField(label='gender',widget=forms.RadioSelect, choices=CHOICES)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email',
                  'photo', 'password1', 'check69', 'password2')
