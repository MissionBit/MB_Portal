from django.shortcuts import render
from home.decorators import group_required
from home.models.models import Announcement


@group_required("student")
def student(request):
    announcements = Announcement.objects.filter(recipient_groups=1)
    return render(request, "student.html", {'announcements': announcements})
