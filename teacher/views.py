from django.shortcuts import render, redirect
from home.decorators import group_required
from home.models.models import Announcement, Form, Notification
from staff.staff_views_helper import mark_announcement_dismissed, remove_dismissed_announcements, \
    remove_submitted_forms, mark_notification_acknowledged
import os
from django.http import HttpResponse, Http404


@group_required("teacher")
def teacher(request):
    if request.method == "POST":
        if request.POST.get("dismiss_announcement") == "true":
            mark_announcement_dismissed(Announcement.objects.get(id=request.POST.get("announcement")), request.user)
            return redirect("teacher")
        elif request.POST.get("acknowledge_notification") == "true":
            mark_notification_acknowledged(Notification.objects.get(id=request.POST.get("notification")))
            return redirect("teacher")
    announcements = Announcement.objects.filter(recipient_groups=4)
    announcements = remove_dismissed_announcements(announcements, request.user)
    forms = Form.objects.filter(recipient_groups=4)
    forms = remove_submitted_forms(forms, request.user)
    notifications = Notification.objects.filter(user_id=request.user.id)
    return render(request, "teacher.html", {"announcements": announcements,
                                            "forms": forms,
                                            "notifications": notifications})


@group_required("teacher")
def download_form(request):
    path = request.GET.get("path")
    file_path = os.path.join(path)
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="pdf/text")
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
            return response
    raise Http404
