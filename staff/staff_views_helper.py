from django.contrib.auth.models import User as DjangoUser
from home.models.salesforce import ClassEnrollment
from home.models.models import UserProfile, Classroom
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages


def create_user_with_profile(form, random_password):
    new_user = DjangoUser.objects.create_user(
        username="%s.%s"
                 % (form.cleaned_data.get("first_name"), form.cleaned_data.get("last_name")),
        email=form.cleaned_data.get("email"),
        first_name=form.cleaned_data.get("first_name"),
        last_name=form.cleaned_data.get("last_name"),
        password=random_password,
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


def setup_classroom_teachers(request, form):
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
    teacher_email_list = [
        DjangoUser.objects.get(id=classroom.teacher_id).email,
        DjangoUser.objects.get(id=classroom.teacher_assistant_id).email
    ]
    enroll_in_class(form, form.cleaned_data.get("teacher"))
    enroll_in_class(form, form.cleaned_data.get("teacher_assistant"))
    email_classroom(request, teacher_email_list, classroom.course)
    return classroom


def add_volunteers_and_students_to_classroom(request, form, classroom):
    email_list = []
    for volunteer in form.cleaned_data.get("volunteers"):
        enroll_in_class(form, volunteer)
        django_user = (
            UserProfile.objects.filter(salesforce_id=volunteer.client_id)
                .first()
                .user_id
        )
        classroom.volunteers.add(django_user)
        email_list.append(DjangoUser.objects.get(id=django_user).email)
    for student in form.cleaned_data.get("students"):
        enroll_in_class(form, student)
        django_user = (
            UserProfile.objects.filter(salesforce_id=student.client_id)
                .first()
                .user_id
        )
        classroom.students.add(django_user)
        email_list.append(DjangoUser.objects.get(id=django_user).email)
    email_classroom(request, email_list, classroom.course)


def email_new_user(request, first_name, account_type, username, password):
    subject = "%s - Your Mission Bit %s Account Has Been Set Up" % (first_name, account_type)
    message = "%s -\n\n\t Welcome to Mission Bit, you are officially our newest %s." \
              "We look forward to introducing you to the rest of your team!  " \
              "You can now log in to your account at: %s.\nYour password has been" \
              "randomly generated, please use it to create your own password, or login with" \
              "your GMAIL account.\n\n\nHere's your username: %s \nHere's your password: %s"\
              % (first_name, account_type, "localhost:8000/", username, password)
    email_from = settings.EMAIL_HOST_USER
    recipient_list = ['tyler.iams@gmail.com']
    send_mail(subject, message, email_from, recipient_list)
    messages.add_message(request, messages.SUCCESS, "Email sent successfully")


def email_classroom(request, email_list, classroom_name):
    subject = "Your Mission Bit %s Classroom Has Been Created" % classroom_name
    message = "Hello,\n" \
              "\tYour %s classroom has been created. Log in to your Mission Bit Web Portal to view!\n\n" \
              "\tSigned, \n\t\t The Mission Bit Web Portal" % classroom_name
    email_from = settings.EMAIL_HOST_USER
    recipient_list = ['tyler.iams@gmail.com', 'iams.sophia@gmail.com']  # REPLACE WITH email_list
    send_mail(subject, message, email_from, recipient_list)
    messages.add_message(request, messages.SUCCESS, "Email sent successfully")

