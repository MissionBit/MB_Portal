from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Contact, User

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(label='email', max_length=100)
    first_name = forms.CharField(label='First name', max_length=100)
    last_name = forms.CharField(label='Last name', max_length=100)
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']


class CreateStaffForm(forms.ModelForm):
    email = forms.EmailField(label='email', max_length=100)
    first_name = forms.CharField(label='First name', max_length=100)
    last_name = forms.CharField(label='Last name', max_length=100)
    birthdate = forms.DateField(label = 'birthday')
    mailing_street = forms.CharField(label = 'street', max_length=100)
    mailing_city = forms.CharField(label = 'city', max_length=100)
    mailing_state = forms.CharField(label = 'state', max_length=100)
    mailing_postal_code = forms.CharField(label = 'zip', max_length=100)
    class Meta:
        model = Contact
        fields = ['email', 'first_name', 'last_name', 'mailing_street','mailing_city', 
        'mailing_state', 'mailing_postal_code', 'mobile_phone', 'birthdate']