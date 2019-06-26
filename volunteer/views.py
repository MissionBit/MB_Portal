from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
def volunteer(request):
    if not request.user.groups.filter(name="volunteer").exists():
        return HttpResponse("Unauthorized", status=401)
    return render(request, "volunteer.html")
