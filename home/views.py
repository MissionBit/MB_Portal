from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from .forms import UserRegisterForm
from .models import Users
from django.contrib import messages

@login_required
def home(request):
	if (request.method == 'POST'):
		first_name = request.POST['firstname']
		last_name = request.POST['lastname']
		role = request.POST['role']
		new_user = Users(
				username = request.user.username,
				email = request.user.email,
				first_name = first_name,
				last_name = last_name,
				role = role
				)
		new_user.save()
		return redirect('home-home')
	else:
		user = Users.objects.filter(email = str(request.user.email)).first()
		if user is None:
			# User should only be able to get here if they logged in with google AND they haven't registered with MB yet
			return render(request, 'home/register_after_oauth.html')
		elif user.role == 'staff':
			return redirect('staff')
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


@login_required
def student(request):
	if Users.objects.filter(email = str(request.user.email)).first().role != 'student':
		return HttpResponse('Unauthorized', status=401)
	return render(request, 'home/student.html')

@login_required
def teacher(request):
	if Users.objects.filter(email = str(request.user.email)).first().role != 'teacher':
		return HttpResponse('Unauthorized', status=401)
	return render(request, 'home/teacher.html')

@login_required
def volunteer(request):
	if Users.objects.filter(email = str(request.user.email)).first().role != 'volunteer':
		return HttpResponse('Unauthorized', status=401)
	return render(request, 'home/volunteer.html')

def logout(request):
	return render(request, 'home/logout.html')

def login(request):
	return render(request, 'home/login.html')

def register(request):
	return render(request, 'home/register.html')

def landing_page(request):
	return render(request, 'home/landing_page.html')

def register_as_student(request):
	if request.method == 'POST':
		form = UserRegisterForm(request.POST)
		if form.is_valid():
			new_user = Users(
				username = form.cleaned_data.get('username'),
				email = form.cleaned_data.get('email'),
				first_name = form.cleaned_data.get('first_name'),
				last_name = form.cleaned_data.get('last_name'),
				role = 'student'
				)
			new_user.save()
			form.save()
			first_name = form.cleaned_data.get('first_name')
			messages.success(request, f'Student Account Successfully Created For {first_name}, please log in')
			return redirect('login')
		return render(request, 'home/register_as_student.html', {'form': form})
	else:
		form = UserRegisterForm()
		return render(request, 'home/register_as_student.html', {'form' : form})

def register_as_volunteer(request):
	if request.method == 'POST':
		form = UserRegisterForm(request.POST)
		if form.is_valid():
			new_user = Users(
				username = form.cleaned_data.get('username'),
				email = form.cleaned_data.get('email'),
				first_name = form.cleaned_data.get('first_name'),
				last_name = form.cleaned_data.get('last_name'),
				role = 'volunteer'
				)
			new_user.save()
			form.save()
			first_name = form.cleaned_data.get('first_name')
			messages.success(request, f'Volunteer Account Successfully Created For {first_name}, please log in')
			return redirect('login')
		return render(request, 'home/register_as_volunteer.html', {'form': form})
	else:
		form = UserRegisterForm()
		return render(request, 'home/register_as_volunteer.html', {'form' : form})
