from django.shortcuts import render
from home.decorators import group_required


@group_required('student')
def student(request):
    return render(request, "student.html")
