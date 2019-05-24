from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm

# Create your views here.
def register(request):
	if request.method == 'POST':
		form = UserRegisterForm(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data.get('username')
			messages.success(request, f'Account Successfully Created For {username}, please log in')
			return redirect('login')
	else:
		form = UserRegisterForm()

	return render(request, 'Users/register.html', {'form' : form})

@login_required
def profile(request):
	return render(request, 'users/profile.html')