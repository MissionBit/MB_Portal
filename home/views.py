from __future__ import unicode_literals
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth import logout
from django.contrib.auth.models import User, Group, Permission
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from .forms import UserRegisterForm
from django.contrib import messages
from urllib.parse import urlencode
from django.urls import reverse
from .models import Contact, User, Individual, ClassOffering, ClassEnrollment

'''
**THIS index() method WILL NOT BE USED IN PRODUCTION: **
it is a method that was added to test the mb-salesforce database 
connection during development
This method should be used to test our database, we can push data to it through here via a
post request and we can query the database from here as well.  Leave this method here for
ease of fxnality testing purposes
until we are ready to deploy in production. 
'''
def index(request):
    # Get ten Contacts
    contacts = Contact.objects.all()
    users = User.objects.all()
    individuals = Individual.objects.all()
    classes = ClassOffering.objects.all()
    enrollments = ClassEnrollment.objects.all()
    context = {
        'contacts': contacts,
        'users' : users,
        'individuals' : individuals,
        'classes' : classes,
        'enrollments' : enrollments
    }
    return render(request, 'home/index.html', context)

'''
If the request's user already has a tag they are redirected to the correct page.  When a user
first logs in they don't have a tag and they are directed based on the group they belong to with
approximately the highest permission level.  If the user wants to use the app as a member of
a different group, they can change in their profile, their tag will be changed and this method 
will be called with a reqeust.user with a tag.
redirects ref:
https://realpython.com/django-redirects/#django-redirects-a-super-simple-example
'''
@login_required
def home(request):
    if request.GET.get('tag') != None:
        return redirect(str(request.GET.get('tag')))
    else:
        if request.user.groups.all().count() == 0:
            return redirect('login') # TEMPORARY
        elif request.user.groups.filter(name = 'staff').exists(): 
            return redirect('staff')
        elif request.user.groups.filter(name = 'teacher').exists():
            return redirect('teacher')
        elif request.user.groups.filter(name = 'volunteer').exists():
            return redirect('volunteer')
        else: #request.user.groups.filter(name = 'student').exists()    
            return redirect('student')

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
            new_user = User.objects.create_user(
                username = form.cleaned_data.get('username'),
                email = form.cleaned_data.get('email'),
                first_name = form.cleaned_data.get('first_name'),
                last_name = form.cleaned_data.get('last_name'),
                password = form.cleaned_data.get('password1')
                )
            student_group = Group.objects.get(name = 'student')
            student_group.user_set.add(new_user)
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
            new_user = User.objects.create_user(
                username = form.cleaned_data.get('username'),
                email = form.cleaned_data.get('email'),
                first_name = form.cleaned_data.get('first_name'),
                last_name = form.cleaned_data.get('last_name'),
                password = form.cleaned_data.get('password1')
                )
            volunteer_group = Group.objects.get(name = 'volunteer')
            volunteer_group.user_set.add(new_user)
            first_name = form.cleaned_data.get('first_name')
            messages.success(request, f'Volunteer Account Successfully Created For {first_name}, please log in')
            return redirect('login')
        return render(request, 'home/register_as_volunteer.html', {'form': form})
    else:
        form = UserRegisterForm()
        return render(request, 'home/register_as_volunteer.html', {'form' : form})
