from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth.models import User as DjangoUser
from .models import Contact, User, Account, Classroom, ClassOffering, ClassEnrollment
from home.choices import *


class UserRegisterForm(UserCreationForm):
    username = forms.CharField(label='Choose Username', max_length=100)
    email = forms.EmailField(label='email', max_length=100)
    first_name = forms.CharField(label='First name', max_length=100)
    last_name = forms.CharField(label='Last name', max_length=100)

    class Meta:
        model = DjangoUser
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']


class CreateStaffForm(forms.ModelForm):
    email = forms.EmailField(label='email', max_length=100)
    first_name = forms.CharField(label='First name', max_length=100)
    last_name = forms.CharField(label='Last name', max_length=100)
    birthdate = forms.DateField(label='birthday')
    title = forms.CharField(initial='Staff', disabled=True)
    owner = forms.ModelChoiceField(queryset =User.objects.filter(is_active=True))
    account = forms.ModelChoiceField(queryset=Account.objects.all(), required=False)

    class Meta:
        model = Contact  
        fields = ['email', 'first_name', 'last_name', 'birthdate', 'owner', 'title']


class CreateStudentForm(forms.ModelForm):
    email = forms.EmailField(label='email', max_length=100)
    first_name = forms.CharField(label='First name', max_length=100)
    last_name = forms.CharField(label='Last name', max_length=100)
    birthdate = forms.DateField(label='birthday')
    title = forms.CharField(initial='Student', disabled=True)
    owner = forms.ModelChoiceField(queryset=User.objects.filter(is_active=True))
    account = forms.ModelChoiceField(queryset=Account.objects.all(), required=False)
    which_best_describes_your_ethnicity = forms.ChoiceField(
        label='Which best describes the Student\'s ethnicity? - Optional',
        choices=ETHNICITY_CHOICES, required=False)
    race = forms.ChoiceField(label='Which best describes the Student\'s race? - Optional', choices=RACE_CHOICES,
                             required=False)
    gender = forms.ChoiceField(label = 'Gender - Optional', choices=GENDER_CHOICES, required=False)
    expected_graduation_year = forms.ChoiceField(label='Expected graduation year', choices=GRAD_YEAR_CHOICES,
                                                 required=False)

    class Meta:
        model = Contact  
        fields = ['email', 'first_name', 'last_name', 'birthdate', 'owner', 'title']


class CreateTeacherForm(forms.ModelForm):
    email = forms.EmailField(label='email', max_length=100)
    first_name = forms.CharField(label='First name', max_length=100)
    last_name = forms.CharField(label='Last name', max_length=100)
    birthdate = forms.DateField(label='birthday')
    title = forms.CharField(initial='Teacher', disabled=True)
    owner = forms.ModelChoiceField(queryset=User.objects.filter(is_active=True))
    which_best_describes_your_ethnicity = forms.ChoiceField(
        label='Which best describes the Teacher\'s ethnicity? - Optional',
        choices=ETHNICITY_CHOICES, required=False)
    race = forms.ChoiceField(label='Which best describes the Teacher\'s race? - Optional',
                             choices=RACE_CHOICES, required=False)
    gender = forms.ChoiceField(label='Gender - Optional', choices=GENDER_CHOICES, required=False)

    class Meta:
        model = Contact
        fields = ['email', 'first_name', 'last_name', 'birthdate', 'owner', 'title']


class CreateVolunteerForm(forms.ModelForm):
    email = forms.EmailField(label='email', max_length=100)
    first_name = forms.CharField(label='First name', max_length=100)
    last_name = forms.CharField(label='Last name', max_length=100)
    birthdate = forms.DateField(label='birthday')
    title = forms.CharField(initial='Volunteer', disabled=True)
    owner = forms.ModelChoiceField(queryset=User.objects.filter(is_active=True))
    which_best_describes_your_ethnicity = forms.ChoiceField(
        label='Which best describes the Volunteer\'s ethnicity? - Optional',
        choices=ETHNICITY_CHOICES, required=False)
    race = forms.ChoiceField(label='Which best describes the Volunteer\'s race? - Optional',
                             choices=RACE_CHOICES, required=False)
    gender = forms.ChoiceField(label='Gender - Optional', choices=GENDER_CHOICES, required=False)

    class Meta:
        model = Contact
        fields = ['email', 'first_name', 'last_name', 'birthdate', 'owner', 'title']


class CreateClassroomForm(forms.ModelForm):
    course = forms.ModelChoiceField(queryset=ClassOffering.objects.all())
    teacher = forms.ModelChoiceField(queryset=Contact.objects.filter(title='Teacher', is_deleted=False))
    teacher_assistant = forms.ModelChoiceField(queryset=Contact.objects.filter(title='Teacher', is_deleted=False))
    volunteers = forms.ModelMultipleChoiceField(queryset=Contact.objects.filter(title='Volunteer', is_deleted=False))
    students = forms.ModelMultipleChoiceField(queryset=Contact.objects.filter(title='Student', is_deleted=False))
    created_by = forms.ModelChoiceField(queryset=User.objects.filter(is_active=True))

    class Meta:
        model = ClassEnrollment
        fields = ['course', 'teacher', 'teacher_assistant', 'volunteers', 'students']


class ChangePwdForm(PasswordChangeForm):
    old_password = forms.CharField(widget = forms.PasswordInput, initial = "missionbit")

    class Meta:
        model = User
        fields = ['old_password', 'new_password1', 'new_password2']
        widgets = {
            'password': forms.PasswordInput(),
        }
