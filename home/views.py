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
		if user is None:
			return render(request, 'home/register.html')
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
