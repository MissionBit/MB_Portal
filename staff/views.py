from django.template.defaulttags import register
from django.shortcuts import render, redirect
from home.decorators import group_required
from django.http import HttpResponse, Http404
from home.forms import (
    CreateStaffForm,
    CreateClassroomForm,
    CreateTeacherForm,
    CreateVolunteerForm,
    CreateStudentForm,
    CreateClassOfferingForm,
    MakeAnnouncementForm,
    ChangeTeacherForm,
    PostFormForm,
    CreateEsignForm,
    CollectForms,
    NotifyUnsubmittedUsersForm,
    AddCurriculumForm,
    AddForumForm,
    AddVolunteerForm,
    AddStudentForm,
)
from .staff_views_helper import *
from attendance.views import get_date_from_template_returned_string
from home.models.models import Classroom, Form, Esign, Notification, Announcement
from .tasks import cross_reference_classrooms_with_class_offerings, reset_classroom_data
from django.db import transaction
from django_q.models import Schedule
from datetime import datetime
from pytz import timezone as tz
import os


@group_required("staff")
def staff(request):
    if request.method == "POST":
        if request.POST.get("dismiss_announcement") == "true":
            mark_announcement_dismissed(
                Announcement.objects.get(id=request.POST.get("announcement")),
                request.user,
            )
            return redirect("staff")
        elif request.POST.get("acknowledge_notification") == "true":
            mark_notification_acknowledged(
                Notification.objects.get(id=request.POST.get("notification"))
            )
            return redirect("staff")
    announcements = get_my_announcements(request, "staff")
    forms = get_my_forms(request, "staff")
    notifications = Notification.objects.filter(
        user_id=request.user.id, acknowledged=False
    )
    return render(
        request,
        "staff.html",
        {
            "announcements": announcements,
            "forms": forms,
            "notifications": notifications,
        },
    )


@group_required("staff")
def classroom_management(request):
    class_dict = {}
    classroom_list = Classroom.objects.all()
    for classroom in classroom_list:
        class_dict.update({classroom.course: get_class_member_dict(classroom)})
    return render(
        request,
        "classroom_management.html",
        {
            "classrooms": classroom_list,
            "class_dicts": class_dict,
            "user_groups": set(
                request.user.groups.all().values_list("name", flat=True)
            ),
        },
    )


@group_required("staff")
def create_staff_user(request):
    if request.method == "POST":
        form = CreateStaffForm(request.POST)
        if form.is_valid():
            save_user_to_salesforce(request, form)
            create_mission_bit_user(request, form, "staff")
            messages.add_message(request, messages.SUCCESS, "Staff User Created")
            return redirect("staff")
        else:
            return render(
                request,
                "create_staff_user.html",
                {
                    "form": form,
                    "user_groups": set(
                        request.user.groups.all().values_list("name", flat=True)
                    ),
                },
            )
    form = CreateStaffForm()
    return render(
        request,
        "create_staff_user.html",
        {
            "form": form,
            "user_groups": set(
                request.user.groups.all().values_list("name", flat=True)
            ),
        },
    )


@group_required("staff")
def create_teacher_user(request):
    if request.method == "POST":
        form = CreateTeacherForm(request.POST)
        if form.is_valid():
            save_user_to_salesforce(request, form)
            create_mission_bit_user(request, form, "teacher")
            messages.add_message(request, messages.SUCCESS, "Teacher User Created")
            return redirect("staff")
        else:
            return render(request, "create_teacher_user.html", {"form": form})
    form = CreateTeacherForm()
    return render(request, "create_teacher_user.html", {"form": form})


@group_required("staff")
def create_student_user(request):
    if request.method == "POST":
        form = CreateStudentForm(request.POST)
        if form.is_valid():
            form.save()
            create_mission_bit_user(request, form, "student")
            messages.add_message(request, messages.SUCCESS, "Student User Created")
            return redirect("staff")
        else:
            return render(request, "create_student_user.html", {"form": form})
    form = CreateStudentForm()
    return render(request, "create_student_user.html", {"form": form})


@group_required("staff")
def create_volunteer_user(request):
    if request.method == "POST":
        form = CreateVolunteerForm(request.POST)
        if form.is_valid():
            save_user_to_salesforce(request, form)
            create_mission_bit_user(request, form, "volunteer")
            messages.add_message(request, messages.SUCCESS, "Volunteer User Created")
            return redirect("staff")
        else:
            return render(request, "create_volunteer_user.html", {"form": form})
    form = CreateVolunteerForm()
    return render(request, "create_volunteer_user.html", {"form": form})


@group_required("staff")
def create_classroom(request):
    if request.method == "POST":
        form = CreateClassroomForm(request.POST)
        if form.is_valid():
            setup_classroom(request, form)
            messages.success(
                request, f'{form.cleaned_data.get("course")} Successfully Created'
            )
            return redirect("staff")
        else:
            return render(request, "create_classroom.html", {"form": form})
    form = CreateClassroomForm()
    return render(request, "create_classroom.html", {"form": form})


@group_required("staff")
def create_class_offering(request):
    if request.method == "POST":
        form = CreateClassOfferingForm(request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(
                request, messages.SUCCESS, "Successfully Added Class Offering"
            )
            return redirect("staff")
        else:
            return render(request, "create_class_offering.html", {"form": form})
    form = CreateClassOfferingForm()
    return render(request, "create_class_offering.html", {"form": form})


@group_required("staff")
def make_announcement(request):
    if request.method == "POST":
        form = MakeAnnouncementForm(request.POST)
        if form.is_valid():
            form.instance.created_by = DjangoUser.objects.get(id=request.user.id)
            user_list = get_users_from_form(form)
            email_list = [user.email for user in user_list]
            if form.instance.email_recipients:
                subject = form.cleaned_data.get("title")
                message = form.cleaned_data.get("announcement")
                email_announcement(request, subject, message, email_list)
            announcement = form.save()
            bulk_distribute_announcement(user_list, announcement)
            messages.add_message(
                request, messages.SUCCESS, "Successfully Made Announcement"
            )
            return redirect("staff")
        else:
            return render(request, "make_announcement.html", {"form": form})
    form = MakeAnnouncementForm(
        initial={"created_by": DjangoUser.objects.get(id=request.user.id)}
    )
    return render(request, "make_announcement.html", {"form": form})


@group_required("staff")
def post_form(request):
    if request.method == "POST":
        form = PostFormForm(request.POST, request.FILES)
        if form.is_valid():
            posted_form = Form(
                name=form.cleaned_data.get("name"),
                description=form.cleaned_data.get("description"),
                form=request.FILES["form"],
                created_by=DjangoUser.objects.get(id=request.user.id),
            )
            if form.cleaned_data.get("esign") is not None:
                posted_form.esign = form.cleaned_data.get("esign")
            posted_form.save()
            posted_form.recipient_groups.set(form.cleaned_data.get("recipient_groups"))
            posted_form.recipient_classrooms.set(
                form.cleaned_data.get("recipient_classrooms")
            )
            user_list = get_users_from_form(form)
            email_list = [user.email for user in user_list]
            if form.cleaned_data.get("email_recipients"):
                subject = form.cleaned_data.get("name")
                message = form.cleaned_data.get("description")
                email_posted_form(
                    request,
                    form.cleaned_data.get("esign", None),
                    subject,
                    message,
                    posted_form,
                    email_list,
                )
            distribute_forms(request, posted_form, user_list)
            messages.add_message(request, messages.SUCCESS, "Successfully Posted Form")
            return redirect("staff")
        else:
            return render(request, "post_form.html", {"form": form})
    form = PostFormForm(
        initial={"created_by": DjangoUser.objects.get(id=request.user.id)}
    )
    return render(request, "post_form.html", {"form": form})


@group_required("staff")
def form_overview(request):
    if request.method == "POST":
        form = CollectForms(request.POST)
        if form.is_valid():
            form_id = Form.objects.get(name=request.POST.get("form_name"))
            form_distribution = FormDistribution.objects.get(
                user_id=request.POST.get("user_id"), form_id=form_id
            )
            form_distribution.submitted = form.cleaned_data.get("submitted")
            form_distribution.save()
            messages.add_message(request, messages.SUCCESS, "Collected Form")
            return redirect("form_overview")
        else:
            return render(request, "form_overview.html", {"form": form})
    outstanding_form_dict = get_outstanding_forms()
    form = CollectForms()
    return render(
        request,
        "form_overview.html",
        {"outstanding_form_dict": outstanding_form_dict, "form": form},
    )


@group_required("staff")
def notify_unsubmitted_users(request, notify_about=None):
    if request.method == "POST":
        form = NotifyUnsubmittedUsersForm(request.POST)
        if form.is_valid():
            print("notify_about: ", request.POST.get("notify_about"))
            form_id = Form.objects.get(name=request.POST.get("notify_about")).id
            form_distributions = FormDistribution.objects.filter(
                form_id=form_id, submitted=False
            )
            for form_dist in form_distributions:
                create_form_notification(request, form, form_dist.user_id)
            if form.cleaned_data.get("email_recipients"):
                email_list = get_emails_from_form_distributions(form_distributions)
                email_form_notification(request, form, email_list)
            messages.add_message(
                request, messages.SUCCESS, "Successfully Notified Users"
            )
            return redirect("staff")
        else:
            return render(request, "notify_unsubmitted_users.html", {"form": form})
    form = NotifyUnsubmittedUsersForm()
    return render(
        request,
        "notify_unsubmitted_users.html",
        {"form": form, "notify_about": notify_about},
    )


@group_required("staff")
def create_form_notification(request, form, user_id):
    notification = Notification(
        subject=form.cleaned_data.get("subject"),
        notification=form.cleaned_data.get("notification"),
        email_recipients=form.cleaned_data.get("email_recipients"),
        created_by=DjangoUser.objects.get(id=request.user.id),
        form_id=Form.objects.get(name=request.POST.get("notify_about")).id,
        user_id=user_id,
    )
    notification.save()


@group_required("staff")
def communication_manager(request):
    if request.method == "POST":
        if request.POST.get("delete_announcement"):
            Announcement.objects.get(id=request.POST.get("announcement_id")).delete()
        elif request.POST.get("delete_notification"):
            Notification.objects.get(id=request.POST.get("notification_id")).delete()
        elif request.POST.get("delete_form"):
            Form.objects.get(id=request.POST.get("form_id")).delete()
        messages.add_message(request, messages.SUCCESS, "Deleted Successfully")
        return redirect("staff")
    announcements = Announcement.objects.all()
    notifications = Notification.objects.all()
    forms = Form.objects.all()
    return render(
        request,
        "communication_manager.html",
        {
            "announcements": announcements,
            "notifications": notifications,
            "forms": forms,
        },
    )


@group_required("staff")
def create_esign(request):
    if request.method == "POST":
        form = CreateEsignForm(request.POST)
        if form.is_valid():
            esign = Esign(
                name=form.cleaned_data.get("name"),
                template=form.cleaned_data.get("link"),
                created_by=DjangoUser.objects.get(id=request.user.id),
            )
            esign.save()
            messages.add_message(
                request, messages.SUCCESS, "Esign Created Successfully"
            )
            return redirect("staff")
        else:
            return render(request, "create_esign.html", {"form": form})
    form = CreateEsignForm(
        initial={"created_by": DjangoUser.objects.get(id=request.user.id)}
    )
    return render(request, "create_esign.html", {"form": form})


@group_required("staff")
def add_forum(request):
    if request.method == "POST":
        form = AddForumForm(request.POST)
        if form.is_valid():
            classroom = Classroom.objects.get(id=request.POST.get("classroom"))
            classroom.forum_title = form.cleaned_data.get("forum_title")
            classroom.forum = form.cleaned_data.get("forum")
            classroom.save()
            messages.add_message(request, messages.SUCCESS, "Forum Added Successfully")
            return redirect("staff")
        else:
            classroom = Classroom.objects.get(id=request.GET.get("classroom"))
            return render(
                request, "add_forum.html", {"form": form, "classroom": classroom}
            )
    classroom = Classroom.objects.get(id=request.GET.get("classroom"))
    form = AddForumForm()
    return render(request, "add_forum.html", {"form": form, "classroom": classroom})


@group_required("staff")
def curriculum(request):
    classroom = Classroom.objects.get(id=request.GET.get("classroom_id"))
    sessions = Session.objects.filter(classroom_id=classroom.id).order_by("date")
    return render(
        request, "curriculum.html", {"sessions": sessions, "classroom": classroom}
    )


@group_required("staff")
def modify_session(request, date=None, classroom=None):
    if request.method == "POST":
        form = AddCurriculumForm(request.POST, request.FILES)
        if form.is_valid():
            update_session(request, form)
            return redirect("classroom_management")
        else:
            date = request.GET.get("date")
            classroom = Classroom.objects.get(id=request.GET.get("classroom"))
            session = Session.objects.get(
                classroom_id=request.GET.get("classroom"),
                date=get_date_from_template_returned_string(request.GET.get("date")),
            )
            return render(
                request,
                "modify_session.html",
                {
                    "form": form,
                    "date": date,
                    "classroom": classroom,
                    "session": session,
                },
            )
    form = AddCurriculumForm()
    date = date
    course = Classroom.objects.get(id=classroom)
    session = Session.objects.get(classroom=classroom, date=date)
    return render(
        request,
        "modify_session.html",
        {"form": form, "date": date, "classroom": course, "session": session},
    )


@group_required("staff")
def classroom_detail(request, course_id):
    if request.method == "POST":
        if request.POST.get("swap_teacher"):
            form = ChangeTeacherForm(request.POST)
            if form.is_valid():
                change_classroom_lead(
                    request.POST.get("fmr_teacher", None),
                    form.cleaned_data.get("teacher").id,
                    request.POST.get("course_id", None),
                    "teacher",
                )
                messages.add_message(
                    request, messages.SUCCESS, "Teacher Successfully Changed"
                )
                return redirect("staff")
            else:
                return render(request, "classroom_detail.html", {"form": form})
        if request.POST.get("swap_teacher_assistant"):
            form = ChangeTeacherForm(request.POST)
            if form.is_valid():
                change_classroom_lead(
                    request.POST.get("fmr_teacher_assistant", None),
                    form.cleaned_data.get("teacher").id,
                    request.POST.get("course_id", None),
                    "teacher_assistant",
                )
                messages.add_message(
                    request, messages.SUCCESS, "Teacher Assistant Successfully Changed"
                )
                return redirect("staff")
            else:
                return render(request, "classroom_detail.html", {"form": form})
        if request.POST.get("remove_student"):  # Input Validation Needed
            remove_user_from_classroom(
                request.POST["fmr_student"], request.POST["course_id"]
            )
            messages.add_message(
                request, messages.SUCCESS, "Student Successfully Removed From Class"
            )
            return redirect("staff")
        if request.POST.get("remove_volunteer"):  # Input Validation Needed
            remove_user_from_classroom(
                request.POST["fmr_volunteer"], request.POST["course_id"]
            )
            messages.add_message(
                request, messages.SUCCESS, "Volunteer Successfully Removed From Class"
            )
            return redirect("staff")
        if request.POST.get("add_volunteer"):
            form = AddVolunteerForm(request.POST)
            if form.is_valid():
                add_user_to_classroom(
                    form.cleaned_data.get("volunteer").id,
                    request.POST["course_id"],
                    "volunteer",
                )
                messages.add_message(
                    request, messages.SUCCESS, "Volunteer Added To Class"
                )
                return redirect("staff")
            else:
                return render(request, "classroom_detail.html", {"form": form})
        if request.POST.get("add_student"):
            form = AddStudentForm(request.POST)
            if form.is_valid():
                add_user_to_classroom(
                    form.cleaned_data.get("student").id,
                    request.POST["course_id"],
                    "student",
                )
                messages.add_message(
                    request, messages.SUCCESS, "Student Added To Class"
                )
                return redirect("staff")
            else:
                messages.add_message(
                    request, messages.ERROR, "Invalid Form"
                )  # Need to have fall through here
                return redirect("staff")
        if request.POST.get("reset_classroom"):
            reset_classroom_data.delay(request.POST.get("classroom"))
            messages.add_message(
                request, messages.SUCCESS, "Revisit page in several minutes to see changes."
            )
            return redirect("classroom_detail", request.POST.get("classroom"))
    classroom = Classroom.objects.get(id=course_id)
    class_members = get_class_member_dict(classroom)
    return render(
        request,
        "classroom_detail.html",
        {
            "change_teacher_form": ChangeTeacherForm(),
            "add_volunteer_form": AddVolunteerForm(),
            "add_student_form": AddStudentForm(),
            "classroom": classroom,
            "class_members": class_members,
        },
    )


@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)
