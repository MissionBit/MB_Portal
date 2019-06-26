from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from home.models import UserProfile
from django.contrib.auth.models import User as DjangoUser
from django.contrib import messages

from home.forms import (
    CreateStaffForm,
    CreateClassroomForm,
    CreateTeacherForm,
    CreateVolunteerForm,
    CreateStudentForm,
    CreateClassOfferingForm,
)
from home.models import (
    Contact,
    ClassEnrollment,
    ClassOffering,
    Classroom,
    User,
    Account,
)


@login_required
def staff(request):
    if not request.user.groups.filter(name="staff").exists():
        return HttpResponse("Unauthorized", status=401)
    return render(request, "staff.html")


@login_required
def user_management(request):
    if not request.user.groups.filter(name="staff").exists():
        return HttpResponse("Unauthorized", status=401)
    return render(request, "user_management.html")


@login_required
def contact_management(request):
    if not request.user.groups.filter(name="staff").exists():
        return HttpResponse("Unauthorized", status=401)
    return render(request, "contact_management.html")


@login_required
def create_staff_user(request):
    if not request.user.groups.filter(name="staff").exists():
        return HttpResponse("Unauthorized", status=401)
    if request.method == "POST":
        form = CreateStaffForm(request.POST)
        if form.is_valid():
            form.save()
            new_user = create_user_with_profile(form)
            staff_group = Group.objects.get(name="staff")
            staff_group.user_set.add(new_user)
            first_name = form.cleaned_data.get("first_name")
            messages.success(
                request, f"Staff Account Successfully Created For {first_name}"
            )
            return redirect("staff")
        else:
            messages.error(
                request,
                "Staff User NOT created, your form was not valid, please try again.",
            )
            return redirect(request, "staff")
    form = CreateStaffForm()
    return render(request, "create_staff_user.html", {"form": form})


@login_required
def create_teacher_user(request):
    if not request.user.groups.filter(name="staff").exists():
        return HttpResponse("Unauthorized", status=401)
    if request.method == "POST":
        form = CreateTeacherForm(request.POST)
        if form.is_valid():
            form.save()
            new_user = create_user_with_profile(form)
            teacher_group = Group.objects.get(name="teacher")
            teacher_group.user_set.add(new_user)
            first_name = form.cleaned_data.get("first_name")
            messages.success(
                request, f"Teacher Account Successfully Created For {first_name}"
            )
            return redirect("staff")
        else:
            messages.error(
                request,
                "Teacher User NOT created, your form was not valid, please try again.",
            )
            return redirect(request, "staff")
    form = CreateTeacherForm()
    return render(request, "create_teacher_user.html", {"form": form})


@login_required
def create_student_user(request):
    if not request.user.groups.filter(name="staff").exists():
        return HttpResponse("Unauthorized", status=401)
    if request.method == "POST":
        form = CreateStudentForm(request.POST)
        if form.is_valid():
            form.save()
            new_user = create_user_with_profile(form)
            student_group = Group.objects.get(name="student")
            student_group.user_set.add(new_user)
            first_name = form.cleaned_data.get("first_name")
            messages.success(
                request, f"Student Account Successfully Created For {first_name}"
            )
            return redirect("staff")
        else:
            messages.error(
                request,
                "Student User NOT created, your form was not valid, please try again.",
            )
            return redirect(request, "staff")
    form = CreateStudentForm()
    return render(request, "create_student_user.html", {"form": form})


@login_required
def create_volunteer_user(request):
    if not request.user.groups.filter(name="staff").exists():
        return HttpResponse("Unauthorized", status=401)
    if request.method == "POST":
        form = CreateVolunteerForm(request.POST)
        if form.is_valid():
            form.save()
            new_user = create_user_with_profile(form)
            volunteer_group = Group.objects.get(name="volunteer")
            volunteer_group.user_set.add(new_user)
            first_name = form.cleaned_data.get("first_name")
            messages.success(
                request, f"Volunteer Account Successfully Created For {first_name}"
            )
            return redirect("staff")
        else:
            messages.error(
                request,
                "Volunteer User NOT created, your form was not valid, please try again.",
            )
            return redirect(request, "staff")
    form = CreateVolunteerForm()
    return render(request, "create_volunteer_user.html", {"form": form})


def create_user_with_profile(form):
    new_user = DjangoUser.objects.create_user(
        username="%s.%s"
        % (form.cleaned_data.get("first_name"), form.cleaned_data.get("last_name")),
        email=form.cleaned_data.get("email"),
        first_name=form.cleaned_data.get("first_name"),
        last_name=form.cleaned_data.get("last_name"),
        password="missionbit",
    )
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
    new_user.save()
    return new_user


@login_required
def create_classroom(request):
    if not request.user.groups.filter(name="staff").exists():
        return HttpResponse("Unauthorized", status=401)
    if request.method == "POST":
        form = CreateClassroomForm(request.POST)
        if form.is_valid():
            classroom = setup_classroom_teachers(form)
            for volunteer in form.cleaned_data.get("volunteers"):
                enroll_in_class(form, volunteer)
                django_user = (
                    UserProfile.objects.filter(salesforce_id=volunteer.client_id)
                    .first()
                    .user_id
                )
                print("volid: %s" % volunteer.id)
                classroom.volunteers.add(django_user)
            for student in form.cleaned_data.get("students"):
                enroll_in_class(form, student)
                django_user = (
                    UserProfile.objects.filter(salesforce_id=student.client_id)
                    .first()
                    .user_id
                )
                print("student id: %s" % student.id)
                print("got user %s from salesforce: " % student)
                classroom.students.add(django_user)
            messages.success(
                request,
                f'Classroom {form.cleaned_data.get("course")} Successfully Created',
            )
            classroom.save()
            return redirect("staff")
    form = CreateClassroomForm()
    return render(request, "create_classroom.html", {"form": form})


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


@login_required
def create_class_offering(request):
    if not request.user.groups.filter(name="staff").exists():
        return HttpResponse("Unauthorized", status=401)
    if request.method == "POST":
        form = CreateClassOfferingForm(request.POST)
        form.save()
        print("FUCK YEAH!!!")
        return redirect("staff")
    form = CreateClassOfferingForm()
    return render(request, "create_class_offering.html", {"form": form})


@login_required
def my_account_staff(request):
    if not request.user.groups.filter(name="staff").exists():
        return HttpResponse("Unauthorized", status=401)
    return render(request, "my_account_staff.html")
