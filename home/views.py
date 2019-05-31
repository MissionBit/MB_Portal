from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from .forms import UserRegisterForm
from .models import Users
from django.contrib import messages

@login_required
def home(request):
    user = Users.objects.filter(email = str(request.user.email)).first()
    if user == None:
        # User should only be able to get here if they logged in with google AND they haven't registered with MB yet
        return redirect('home-register_after_oauth')
    elif user.role == 'staff':
        return redirect('staff')
    elif user.role == 'student':
        return redirect('student')
    elif user.role == 'teacher':
        return redirect('teacher')
    else: #user.role == 'volunteer'
        return redirect('volunteer')

def logout_view(request):
    logout(request)
    return render(request, 'home/logout.html')

def login(request):
    return redirect('login')

def register(request):
    return render(request, 'home/register.html')

def landing_page(request):
    return render(request, 'home/landing_page.html')

def register_after_oauth(request):
    return render(request, 'home/register_after_oauth.html')

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
            new_user.save() #saves to home_users
            form.save()     #saves to auth_users
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
