from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from home.models import Users
from django.shortcuts import render

@login_required
def student(request):
	if Users.objects.filter(email = str(request.user.email)).first().role != 'student':
		return HttpResponse('Unauthorized', status=401)
	return render(request, 'student.html')
