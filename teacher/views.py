from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from django.shortcuts import render

@login_required
def teacher(request):
    if not request.user.groups.filter(name = 'staff').exists():
        return HttpResponse('Unauthorized', status=401)
    return render(request, 'teacher.html')
