from django.shortcuts import render, redirect
from home.decorators import group_required
from home.models.models import (
    Announcement,
    Form,
    Notification,
    Classroom,
    Session,
    Resource,
)
from home.forms import AddResourceForm
from attendance.views import get_date_from_template_returned_string
from staff.staff_views_helper import get_classroom_by_django_user
from staff.staff_views_helper import (
    mark_announcement_dismissed,
    mark_notification_acknowledged,
    get_my_announcements,
    get_my_forms,
)
import os
from django.http import HttpResponse, Http404
from django.contrib import messages


@group_required("teacher")
def teacher(request):
    if request.method == "POST":
        if request.POST.get("dismiss_announcement") == "true":
            mark_announcement_dismissed(
                Announcement.objects.get(id=request.POST.get("announcement")),
                request.user,
            )
            return redirect("teacher")
        elif request.POST.get("acknowledge_notification") == "true":
            mark_notification_acknowledged(
                Notification.objects.get(id=request.POST.get("notification"))
            )
            return redirect("teacher")
    announcements = get_my_announcements(request, "staff")
    forms = get_my_forms(request, "staff")
    notifications = Notification.objects.filter(user_id=request.user.id)
    classroom = get_classroom_by_django_user(request.user)
    return render(
        request,
        "teacher.html",
        {
            "announcements": announcements,
            "forms": forms,
            "notifications": notifications,
            "classroom": classroom,
        },
    )


@group_required("teacher")
def my_class_teacher(request):
    classroom = get_classroom_by_django_user(request.user)
    sessions = Session.objects.filter(classroom_id=classroom.id).order_by("date")
    return render(
        request, "my_class_teacher.html", {"sessions": sessions, "classroom": classroom}
    )


@group_required("teacher")
def session_view_teacher(request):
    if request.method == "POST":
        form = AddResourceForm(request.POST, request.FILES)
        if form.is_valid():
            resource = Resource(
                title=form.cleaned_data.get("title"),
                description=form.cleaned_data.get("description"),
                classroom_id=request.POST.get("classroom"),
                session_id=request.POST.get("session"),
            )
            if request.POST.get("link"):
                resource.link = form.cleaned_data.get("link")
            if request.FILES.get("file"):
                resource.file = form.cleaned_data.get("file")
            resource.save()
            messages.add_message(request, messages.SUCCESS, "Resource Added To Session")
            return redirect("teacher")
        else:
            return render(request, "session_view_teacher.html", {"form": form})
    session = Session.objects.get(
        classroom_id=request.GET.get("classroom"),
        date=get_date_from_template_returned_string(request.GET.get("session_date")),
    )
    resources = Resource.objects.filter(session_id=session.id)
    classroom = get_classroom_by_django_user(request.user)
    form = AddResourceForm()
    return render(
        request,
        "session_view_teacher.html",
        {
            "session": session,
            "resources": resources,
            "form": form,
            "classroom": classroom,
        },
    )
