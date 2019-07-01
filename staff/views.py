from django.views.generic import DetailView, ListView
from django.shortcuts import render, redirect
from django.contrib.auth.models import Group
from home.decorators import group_required
from home.forms import (
    CreateStaffForm,
    CreateClassroomForm,
    CreateTeacherForm,
    CreateVolunteerForm,
    CreateStudentForm,
    CreateClassOfferingForm,
    MakeAnnouncementForm,
)
from .staff_views_helper import *


@group_required("staff")
def staff(request):
    return render(request, "staff.html")


@group_required("staff")
def user_management(request):
    return render(request, "user_management.html")


@group_required("staff")
def classroom_management(request):
    all_classrooms = {}
    for classroom in Classroom.objects.all():
        teacher_user = DjangoUser.objects.get(id=classroom.teacher_id)
        teacher_assistant_user = DjangoUser.objects.get(id=classroom.teacher_assistant_id)
        student_list = add_students_to_student_dict(classroom)
        volunteer_list = add_volunteers_to_volunteer_dict(classroom)
        class_dict = {'id': classroom.id,
                      'teacher': "%s %s" % (teacher_user.first_name, teacher_user.last_name),
                      'teacher_assistant': "%s %s" % (teacher_assistant_user.first_name, teacher_assistant_user.last_name),
                      'student_list': student_list,
                      'volunteer_list': volunteer_list
                      }
        all_classrooms[str(classroom.course)] = class_dict

    return render(request, "classroom_management.html", {'classrooms': all_classrooms})


@group_required("staff")
def contact_management(request):
    return render(request, "contact_management.html")


@group_required("staff")
def create_staff_user(request):
    if request.method == "POST":
        form = CreateStaffForm(request.POST)
        if form.is_valid():
            form.save()
            random_password = DjangoUser.objects.make_random_password()
            new_user = create_user_with_profile(form, random_password)
            email = form.cleaned_data.get("email")
            staff_group = Group.objects.get(name="staff")
            staff_group.user_set.add(new_user)
            first_name = form.cleaned_data.get("first_name")
            messages.success(
                request, f"Staff Account Successfully Created For {first_name}"
            )
            email_new_user(
                request, email, first_name, "staff", new_user.username, random_password
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


@group_required("staff")
def create_teacher_user(request):
    if request.method == "POST":
        form = CreateTeacherForm(request.POST)
        if form.is_valid():
            form.save()
            random_password = DjangoUser.objects.make_random_password()
            new_user = create_user_with_profile(form)
            email = form.cleaned_data.get("email")
            teacher_group = Group.objects.get(name="teacher")
            teacher_group.user_set.add(new_user)
            first_name = form.cleaned_data.get("first_name")
            messages.success(
                request, f"Teacher Account Successfully Created For {first_name}"
            )
            email_new_user(
                request,
                email,
                first_name,
                "teacher",
                new_user.username,
                random_password,
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


@group_required("staff")
def create_student_user(request):
    if request.method == "POST":
        form = CreateStudentForm(request.POST)
        if form.is_valid():
            form.save()
            random_password = DjangoUser.objects.make_random_password()
            new_user = create_user_with_profile(form)
            email = form.cleaned_data.get("email")
            student_group = Group.objects.get(name="student")
            student_group.user_set.add(new_user)
            first_name = form.cleaned_data.get("first_name")
            messages.success(
                request, f"Student Account Successfully Created For {first_name}"
            )
            email_new_user(
                request,
                email,
                first_name,
                "student",
                new_user.username,
                random_password,
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


@group_required("staff")
def create_volunteer_user(request):
    if request.method == "POST":
        form = CreateVolunteerForm(request.POST)
        if form.is_valid():
            form.save()
            random_password = DjangoUser.objects.make_random_password()
            new_user = create_user_with_profile(form)
            email = form.cleaned_data.get("email")
            volunteer_group = Group.objects.get(name="volunteer")
            volunteer_group.user_set.add(new_user)
            first_name = form.cleaned_data.get("first_name")
            messages.success(
                request, f"Volunteer Account Successfully Created For {first_name}"
            )
            email_new_user(
                request,
                email,
                first_name,
                "volunteer",
                new_user.username,
                random_password,
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


@group_required("staff")
def create_classroom(request):
    if request.method == "POST":
        form = CreateClassroomForm(request.POST)
        if form.is_valid():
            classroom = setup_classroom_teachers(request, form)
            add_volunteers_and_students_to_classroom(request, form, classroom)
            messages.success(
                request,
                f'Classroom {form.cleaned_data.get("course")} Successfully Created',
            )
            classroom.save()
            return redirect("staff")
        else:
            messages.error(
                request,
                "Classroom NOT created, your form was not valid, please try again.",
            )
            return redirect(request, "staff")
    form = CreateClassroomForm()
    return render(request, "create_classroom.html", {"form": form})


@group_required("staff")
def create_class_offering(request):
    if request.method == "POST":
        form = CreateClassOfferingForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("staff")
        else:
            messages.error(
                request,
                "Class offering NOT created, your form was not valid, please try again.",
            )
            return redirect(request, "staff")
    form = CreateClassOfferingForm()
    return render(request, "create_class_offering.html", {"form": form})


@group_required("staff")
def make_announcement(request):
    if request.method == "POST":
        form = MakeAnnouncementForm(request.POST)
        if form.is_valid():
            form.instance.created_by = DjangoUser.objects.get(id=request.user.id)
            form.save()
            messages.add_message(request, messages.SUCCESS, "Successfully Made Announcement")
            return redirect("staff")
        else:
            messages.error(
                request,
                "Announcement NOT made, your announcement form was not valid, please try again.",
            )
            return redirect(request, "staff")
    form = MakeAnnouncementForm(initial={'created_by': DjangoUser.objects.get(id=request.user.id)})
    return render(request, "make_announcement.html", {"form": form})


@group_required("staff")
def my_account_staff(request):
    return render(request, "my_account_staff.html")


class ClassroomDetailView(DetailView):
    model = Classroom


class ClassroomListView(ListView):
    model = Classroom
    template_name = 'classroom_management.html'
    context_object_name = 'classrooms'

