from django.shortcuts import render
from home.decorators import group_required


@group_required('volunteer')
def volunteer(request):
    return render(request, "volunteer.html")
