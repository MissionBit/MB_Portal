from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterForm

# Create your views here.
def register(request):
	if request.method == 'POST':
		form = UserRegisterForm(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data.get('username')
			messages.success(request, f'Account Successfully Created For {username}')
			return redirect('blog-home')
	else:
		form = UserRegisterForm()
	
	return render(request, 'Users/register.html', {'form' : form})