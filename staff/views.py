from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from home.models import Users

@login_required
def staff(request):
	if Users.objects.filter(email = str(request.user.email)).first().role != 'staff':
		return HttpResponse('Unauthorized', status=401)
	return render(request, 'staff.html')

@login_required
def user_management(request):
	if Users.objects.filter(email = str(request.user.email)).first().role != 'staff':
		return HttpResponse('Unauthorized', status=401)
	return render(request, 'user_management.html')

@login_required
def create_staff_user(request):
	if Users.objects.filter(email = str(request.user.email)).first().role != 'staff':
		return HttpResponse('Unauthorized', status=401)
	return render(request, 'create_staff_user.html')

@login_required
def create_teacher_user(request):
	if Users.objects.filter(email = str(request.user.email)).first().role != 'staff':
		return HttpResponse('Unauthorized', status=401)
	return render(request, 'create_teacher_user.html')

@login_required
def create_student_user(request):
	if Users.objects.filter(email = str(request.user.email)).first().role != 'staff':
		return HttpResponse('Unauthorized', status=401)
	return render(request, 'create_student_user.html')

@login_required
def create_volunteer_user(request):
	if Users.objects.filter(email = str(request.user.email)).first().role != 'staff':
		return HttpResponse('Unauthorized', status=401)
	return render(request, 'create_volunteer_user.html')

@login_required
def my_account_staff(request):
	if Users.objects.filter(email = str(request.user.email)).first().role != 'staff':
		return HttpResponse('Unauthorized', status=401)
	return render(request, 'my_account_staff.html')

