from django.shortcuts import render
from home.decorators import group_required


@group_required('teacher')
def teacher(request):
    return render(request, "teacher.html")
