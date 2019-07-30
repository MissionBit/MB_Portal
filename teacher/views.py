from django.shortcuts import render, redirect
from home.decorators import group_required
from home.models.models import Announcement, Form
import os
from django.http import HttpResponse, Http404


@group_required("teacher")
def teacher(request):
    announcements = Announcement.objects.filter(recipient_groups=4)
    forms = Form.objects.filter(recipient_groups=4)
    return render(request, "teacher.html", {"announcements": announcements,
                                            "forms": forms})


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
