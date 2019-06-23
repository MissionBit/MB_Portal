from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
def donor(request):
    if not request.user.groups.filter(name='donor').exists():
        return HttpResponse('Unauthorized', status=401)
    return render(request, 'donor.html')
