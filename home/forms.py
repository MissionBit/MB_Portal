from django import forms
from django.contrib.auth.models import User as postgresUser
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
    owner = forms.ModelChoiceField(queryset=User.objects.all())
    class Meta:
        model = Contact   
        fields = ['email', 'first_name', 'last_name', 'birthdate', 'owner']