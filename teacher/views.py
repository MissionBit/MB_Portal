from django.shortcuts import render
from home.decorators import group_required
from home.models.models import Announcement


@group_required("teacher")
def teacher(request):
    announcements = Announcement.objects.filter(recipient_groups=2)
    return render(request, "teacher.html", {'announcements': announcements})
