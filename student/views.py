from django.shortcuts import render, redirect
from home.decorators import group_required
from home.models.models import Announcement, Form
import os
from django.conf import settings
from django.http import HttpResponse, Http404


@group_required("student")
def student(request):
    announcements = Announcement.objects.filter(recipient_groups=1)
    forms = Form.objects.filter(recipient_groups=1)
    return render(request, "student.html", {"announcements": announcements,
                                            "forms": forms})


@group_required("student")
def download_form(request):
    path = request.GET.get("path")
    file_path = os.path.join(path)
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="pdf/text")
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
            return response
    raise Http404
