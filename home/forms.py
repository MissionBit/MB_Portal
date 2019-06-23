from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from .models import Contact, User
from django.contrib.auth.models import User as django_user

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
    title = forms.CharField(initial = "Staff", disabled=True)
    owner = forms.ModelChoiceField(queryset = User.objects.filter(is_active = True))
    class Meta:
        model = Contact  
        fields = ['email', 'first_name', 'last_name', 'birthdate', 'owner', 'title']

class ChangePwdForm(PasswordChangeForm):
	old_password = forms.CharField(widget = forms.PasswordInput, initial = "missionbit")
	class Meta:
		model = User
		fields = ['old_password', 'new_password1', 'new_password2']
		widgets = {
            'password': forms.PasswordInput(),
        }