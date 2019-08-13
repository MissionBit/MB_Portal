from django.shortcuts import render
from home.decorators import group_required


@group_required("volunteer")
def volunteer(request):
    #  New comment here
    return render(request, "volunteer.html")
