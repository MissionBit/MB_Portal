from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from home.models import Users
from django.shortcuts import render

@login_required
def volunteer(request):
	if Users.objects.filter(email = str(request.user.email)).first().role != 'volunteer':
		return HttpResponse('Unauthorized', status=401)
	return render(request, 'volunteer.html')
