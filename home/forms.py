from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth.models import User as DjangoUser
from django.contrib.auth.models import Group
from home.models.models import Announcement, Classroom
from home.models.salesforce import (
    Contact,
    User,
    Account,
    ClassOffering,
    ClassEnrollment,
)
from home.choices import *


class UserRegisterForm(UserCreationForm):
    username = forms.CharField(label="Choose Username", max_length=100)
    email = forms.EmailField(label="email", max_length=100)
    first_name = forms.CharField(label="First name", max_length=100)
    last_name = forms.CharField(label="Last name", max_length=100)

    class Meta:
        model = DjangoUser
        fields = [
            "username",
            "email",
            "first_name",
            "last_name",
            "password1",
            "password2",
        ]


class MissionBitUserCreationForm(forms.ModelForm):
    account = forms.ModelChoiceField(queryset=Account.objects.all(), required=False)
    first_name = forms.CharField(label="First name", max_length=100)
    last_name = forms.CharField(label="Last name", max_length=100)
    email = forms.EmailField(label="email", max_length=100)
    birthdate = forms.DateField(label="birthday")
    owner = forms.ModelChoiceField(queryset=User.objects.filter(is_active=True))

    class Meta:
        model = Contact
        fields = []


class RaceGenderEthnicityForm(forms.ModelForm):
    which_best_describes_your_ethnicity = forms.ChoiceField(
        label="Ethnicity - Optional", choices=ETHNICITY_CHOICES, required=False
    )
    race = forms.ChoiceField(
        label="Race - Optional", choices=RACE_CHOICES, required=False
    )
    gender = forms.ChoiceField(
        label="Gender - Optional", choices=GENDER_CHOICES, required=False
    )

    class Meta:
        model = Contact
        fields = []


class CreateStaffForm(MissionBitUserCreationForm):
    title = forms.CharField(initial="Staff", disabled=True)

    class Meta:
        model = Contact
        fields = [
            "account",
            "first_name",
            "last_name",
            "email",
            "birthdate",
            "owner",
            "title",
        ]


class CreateStudentForm(RaceGenderEthnicityForm, MissionBitUserCreationForm):
    title = forms.CharField(initial="Student", disabled=True)
    expected_graduation_year = forms.ChoiceField(
        label="Expected graduation year", choices=GRAD_YEAR_CHOICES, required=False
    )
    npsp_primary_affiliation = forms.ModelChoiceField(
        label="Affiliated Account", queryset=Account.objects.all(), required=False
    )

    class Meta:
        model = Contact
        fields = [
            "account",
            "first_name",
            "last_name",
            "email",
            "birthdate",
            "owner",
            "title",
            "expected_graduation_year",
            "npsp_primary_affiliation",
            "which_best_describes_your_ethnicity",
            "race",
            "gender",
        ]


class CreateTeacherForm(RaceGenderEthnicityForm, MissionBitUserCreationForm):
    title = forms.CharField(initial="Teacher", disabled=True)

    class Meta:
        model = Contact
        fields = [
            "account",
            "first_name",
            "last_name",
            "email",
            "birthdate",
            "owner",
            "title",
            "which_best_describes_your_ethnicity",
            "race",
            "gender",
        ]


class CreateVolunteerForm(RaceGenderEthnicityForm, MissionBitUserCreationForm):
    title = forms.CharField(initial="Volunteer", disabled=True)

    class Meta:
        model = Contact
        fields = [
            "account",
            "first_name",
            "last_name",
            "email",
            "birthdate",
            "owner",
            "title",
            "which_best_describes_your_ethnicity",
            "race",
            "gender",
        ]


class CreateClassroomForm(forms.ModelForm):
    course = forms.ModelChoiceField(queryset=ClassOffering.objects.all())
    teacher = forms.ModelChoiceField(
        queryset=Contact.objects.filter(title="Teacher", is_deleted=False)
    )
    teacher_assistant = forms.ModelChoiceField(
        queryset=Contact.objects.filter(title="Teacher", is_deleted=False)
    )
    volunteers = forms.ModelMultipleChoiceField(
        widget=forms.CheckboxSelectMultiple(),
        queryset=Contact.objects.filter(title="Volunteer", is_deleted=False),
    )
    students = forms.ModelMultipleChoiceField(
        widget=forms.CheckboxSelectMultiple(),
        queryset=Contact.objects.filter(title="Student", is_deleted=False),
    )
    created_by = forms.ModelChoiceField(queryset=User.objects.filter(is_active=True))

    class Meta:
        model = ClassEnrollment
        fields = ["course", "teacher", "teacher_assistant", "volunteers", "students"]


class CreateClassOfferingForm(forms.ModelForm):
    name = forms.CharField(max_length="80")
    location = forms.ModelChoiceField(
        queryset=Account.objects.filter(npe01_systemis_individual=False)
    )
    created_by = forms.ModelChoiceField(queryset=User.objects.filter(is_active=True))
    start_date = forms.DateField(label="Start Date")
    end_date = forms.DateField(label="End Date")
    description = forms.CharField(label="Description", max_length=100)
    instructor = forms.ModelChoiceField(
        queryset=Contact.objects.filter(title="Teacher", is_deleted=False)
    )
    meeting_days = forms.ChoiceField(label="Meeting Days", choices=MEETING_DAYS_CHOICES)

    class Meta:
        model = ClassOffering
        fields = [
            "name",
            "location",
            "created_by",
            "start_date",
            "end_date",
            "description",
            "instructor",
            "meeting_days",
        ]

    def __str__(self):
        return "%s" % self.name


class ChangePwdForm(PasswordChangeForm):
    old_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ["old_password", "new_password1", "new_password2"]
        widgets = {"password": forms.PasswordInput()}


class MakeAnnouncementForm(forms.ModelForm):
    title = forms.CharField(max_length=240)
    announcement = forms.Textarea()
    recipient_groups = forms.ModelMultipleChoiceField(
        widget=forms.CheckboxSelectMultiple,
        queryset=Group.objects.all(),
        required=False,
    )
    recipient_classrooms = forms.ModelMultipleChoiceField(
        widget=forms.CheckboxSelectMultiple,
        queryset=Classroom.objects.all(),
        required=False,
    )
    email_recipients = forms.BooleanField(initial=False, required=False)

    class Meta:
        model = Announcement
        fields = [
            "title",
            "announcement",
            "recipient_groups",
            "recipient_classrooms",
            "email_recipients",
        ]


class ChangeTeacherForm(forms.ModelForm):
    teacher = forms.ModelChoiceField(
        queryset=DjangoUser.objects.filter(groups__name="teacher"),
        required=False,
        label="",
    )

    class Meta:
        model = Classroom
        fields = ["teacher"]


class AddVolunteersForm(forms.ModelForm):
    volunteers = forms.ModelMultipleChoiceField(
        widget=forms.CheckboxSelectMultiple,
        queryset=DjangoUser.objects.filter(groups__name="volunteer"),
        required=False,
        label="",
    )

    class Meta:
        model = Classroom
        fields = ["volunteers"]


class AddStudentsForm(forms.ModelForm):
    students = forms.ModelMultipleChoiceField(
        widget=forms.CheckboxSelectMultiple,
        queryset=DjangoUser.objects.filter(groups__name="student"),
        required=False,
        label="",
    )

    class Meta:
        model = Classroom
        fields = ["students"]
