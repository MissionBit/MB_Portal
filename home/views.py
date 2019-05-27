from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Users

@login_required
def home(request):
	if request.method == 'POST':
		create_user(request)
		return redirect('home-home')
	else:
		user = Users.objects.filter(email = str(request.user.email)).first()
		print(user.role == 'staff')
		if user is None:
			return render(request, 'home/register.html')
		elif user.role == 'staff':
			return redirect('home-staff')
		elif user.role == 'student':
			return redirect('home-student')
		elif user.role == 'teacher':
			return redirect('home-teacher')
		elif user.role == 'volunteer':
			return redirect('home-volunteer')
		else: 
			context = {
				'useremail' : user.email
			}
			return render(request, 'home/home.html', context)


def create_user(request):
	first_name = request.POST['first_name']
	last_name = request.POST['last_name']
	role = request.POST['role']
	new_user = Users(
		username = request.user.username,
		email = request.user.email,
		first_name = first_name,
		last_name = last_name,
		role = role
		)
	new_user.save()


def staff(request):
	print()
	if Users.objects.filter(email = str(request.user.email)).first().role != 'staff':
		return HttpResponse('Unauthorized', status=401)
	return render(request, 'home/staff.html')

def student(request):
	if Users.objects.filter(email = str(request.user.email)).first().role != 'student':
		return HttpResponse('Unauthorized', status=401)
	return render(request, 'home/student.html')

def teacher(request):
	if Users.objects.filter(email = str(request.user.email)).first().role != 'teacher':
		return HttpResponse('Unauthorized', status=401)
	return render(request, 'home/teacher.html')

def volunteer(request):
	if Users.objects.filter(email = str(request.user.email)).first().role != 'volunteer':
		return HttpResponse('Unauthorized', status=401)
	return render(request, 'home/volunteer.html')
