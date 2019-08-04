from django.shortcuts import render, redirect
from django.contrib.auth.models import Group
from home.decorators import group_required
from home.models.models import Announcement, Form, Notification, Attendance, Classroom, Session, Resource
from attendance.views import get_average_attendance_from_list, get_date_from_template_returned_string
from staff.staff_views_helper import get_classroom_by_django_user
import os
from staff.staff_views_helper import mark_announcement_dismissed, remove_dismissed_announcements, remove_submitted_forms, mark_notification_acknowledged
from django.http import HttpResponse, Http404
from datetime import datetime


@group_required("student")
def student(request):
    if request.method == "POST":
        if request.POST.get("dismiss_announcement") == "true":
            mark_announcement_dismissed(Announcement.objects.get(id=request.POST.get("announcement")), request.user)
            return redirect("student")
        elif request.POST.get("acknowledge_notification") == "true":
            mark_notification_acknowledged(Notification.objects.get(id=request.POST.get("notification")))
            return redirect("student")
    announcements = Announcement.objects.filter(recipient_groups=Group.objects.get(name="student").id)
    announcements = remove_dismissed_announcements(announcements, request.user)
    forms = Form.objects.filter(recipient_groups=Group.objects.get(name="student").id)
    forms = remove_submitted_forms(forms, request.user)
    notifications = Notification.objects.filter(user_id=request.user.id, acknowledged=False)
    return render(request, "student.html", {"announcements": announcements,
                                            "forms": forms,
                                            "notifications": notifications})


@group_required("student")
def attendance_student(request):
    classroom = get_classroom_by_django_user(request.user)
    attendance = Attendance.objects.filter(student_id=request.user.id,
                                           date__range=["2000-01-01", datetime.today().date()]).order_by("date")
    attendance_percentage = get_average_attendance_from_list(attendance) * 100
    return render(request, "attendance_student.html", {"attendance": attendance,
                                                       "attendance_percentage": attendance_percentage,
                                                       "classroom": classroom})


@group_required("student")
def my_class_student(request):
    classroom = get_classroom_by_django_user(request.user)
    sessions = Session.objects.filter(classroom_id=classroom.id,
                                      date__range=["2000-01-01", datetime.today().date()]).order_by("date")
    return render(request, "my_class_student.html", {"classroom": classroom,
                                                     "sessions": sessions})


@group_required("student")
def session_view_student(request):
    session = Session.objects.get(classroom_id=request.GET.get("classroom"),
                                  date=get_date_from_template_returned_string(request.GET.get("session_date")))
    resources = Resource.objects.filter(session_id=session.id)
    return render(request, "session_view_student.html", {"session": session,
                                                         "resources": resources})
