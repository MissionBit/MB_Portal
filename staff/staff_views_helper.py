from django.contrib.auth.models import User as DjangoUser
from home.models.salesforce import ClassEnrollment
from home.models.models import UserProfile, Classroom


def create_user_with_profile(form):
    new_user = DjangoUser.objects.create_user(
        username="%s.%s"
                 % (form.cleaned_data.get("first_name"), form.cleaned_data.get("last_name")),
        email=form.cleaned_data.get("email"),
        first_name=form.cleaned_data.get("first_name"),
        last_name=form.cleaned_data.get("last_name"),
        password="missionbit",
    )
    new_user = parse_new_user(new_user, form)
    new_user.save()
    return new_user


def parse_new_user(new_user, form):
    birthdate = str(form.cleaned_data.get("birthdate")).replace(r"/", "")
    birthdate_year = birthdate[0:4]
    birthdate_m = birthdate[8:]
    birthdate_d = birthdate[5:7]
    new_user.userprofile.change_pwd = True
    new_user.userprofile.salesforce_id = "%s%s%s%s%s" % (
        form.cleaned_data.get("first_name")[:3],
        form.cleaned_data.get("last_name")[:3],
        birthdate_year,
        birthdate_d,
        birthdate_m,
    )
    new_user.userprofile.date_of_birth = "%s-%s-%s" % (
        birthdate_year,
        birthdate_d,
        birthdate_m,
    )
    return new_user


def enroll_in_class(form, user):
    ClassEnrollment.objects.get_or_create(
        name=form.cleaned_data.get("course"),
        created_by=form.cleaned_data.get("created_by"),
        contact=user,
        status="Enrolled",
        class_offering=form.cleaned_data.get("course"),
    )


def setup_classroom_teachers(form):
    print("teach id: %s" % form.cleaned_data.get("teacher").client_id)
    print("teach id: %s" % form.cleaned_data.get("teacher_assistant").client_id)
    classroom = Classroom.objects.create(
        teacher_id=UserProfile.objects.filter(
            salesforce_id=form.cleaned_data.get("teacher").client_id
        )
        .first()
        .user_id,
        teacher_assistant_id=UserProfile.objects.filter(
            salesforce_id=form.cleaned_data.get("teacher_assistant").client_id
        )
        .first()
        .user_id,
        course=form.cleaned_data.get("course").name,
    )
    enroll_in_class(form, form.cleaned_data.get("teacher"))
    enroll_in_class(form, form.cleaned_data.get("teacher_assistant"))
    return classroom


def add_volunteers_and_students_to_classroom(form):
    for volunteer in form.cleaned_data.get("volunteers"):
        enroll_in_class(form, volunteer)
        django_user = (
            UserProfile.objects.filter(salesforce_id=volunteer.client_id)
                .first()
                .user_id
        )
        classroom.volunteers.add(django_user)
    for student in form.cleaned_data.get("students"):
        enroll_in_class(form, student)
        django_user = (
            UserProfile.objects.filter(salesforce_id=student.client_id)
                .first()
                .user_id
        )
        classroom.students.add(django_user)
