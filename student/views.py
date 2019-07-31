from django.shortcuts import render, redirect
from home.decorators import group_required
from home.models.models import Announcement, Form, Notification
import os
from staff.staff_views_helper import mark_announcement_dismissed, remove_dismissed_announcements, remove_submitted_forms, mark_notification_acknowledged
from django.conf import settings
from django.http import HttpResponse, Http404


@group_required("student")
def student(request):
    if request.method == "POST":
        if request.POST.get("dismiss_announcement") == "true":
            mark_announcement_dismissed(Announcement.objects.get(id=request.POST.get("announcement")), request.user)
            return redirect("student")
        elif request.POST.get("acknowledge_notification") == "true":
            mark_notification_acknowledged(Notification.objects.get(id=request.POST.get("notification")))
            return redirect("student")
    announcements = Announcement.objects.filter(recipient_groups=1)
    announcements = remove_dismissed_announcements(announcements, request.user)
    forms = Form.objects.filter(recipient_groups=1)
    forms = remove_submitted_forms(forms, request.user)
    notifications = Notification.objects.filter(user_id=request.user.id, acknowledged=False)
    return render(request, "student.html", {"announcements": announcements,
                                            "forms": forms,
                                            "notifications": notifications})


@group_required("student")
def download_form_student(request):
    path = request.GET.get("path")
    file_path = os.path.join(path)
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="pdf/text")
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
            return response
    raise Http404
