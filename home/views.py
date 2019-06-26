from __future__ import unicode_literals
from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib.auth.models import Group
from django.contrib.auth.models import User as DjangoUser
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, ChangePwdForm
from django.contrib import messages
from .models import Contact, User, Individual, ClassOffering, ClassEnrollment
from django.contrib.auth import update_session_auth_hash


"""
**THIS index() method WILL NOT BE USED IN PRODUCTION: **
it is a method that was added to test the mb-salesforce database 
connection during development
This method should be used to test our database, we can push data to it through here via a
post request and we can query the database from here as well.  Leave this method here for
ease of fxnality testing purposes
until we are ready to deploy in production. 
"""


def index(request):
    contacts = Contact.objects.all()
    users = User.objects.all()
    individuals = Individual.objects.all()
    classes = ClassOffering.objects.all()
    enrollments = ClassEnrollment.objects.all()
    context = {
        "contacts": contacts,
        "users": users,
        "individuals": individuals,
        "classes": classes,
        "enrollments": enrollments,
    }
    return render(request, "home/index.html", context)


"""
If the request's user already has a tag they are redirected to the correct page.  When a user
first logs in they don't have a tag and they are directed based on the group they belong to with
approximately the highest permission level.  If the user wants to use the app as a member of
a different group, they can change in their profile, their tag will be changed and this method 
will be called with a reqeust.user with a tag.
redirects ref:
https://realpython.com/django-redirects/#django-redirects-a-super-simple-example
"""


@login_required
def home(request):
    if request.user.userprofile.change_pwd:
        return redirect("change_pwd")
    if request.GET.get("tag") is not None:
        return redirect(str(request.GET.get("tag")))
    else:
        if request.user.groups.all().count() == 0:
            return redirect("home-register_after_oauth")  # TEMPORARY
        elif request.user.groups.filter(name="staff").exists():
            return redirect("staff")
        elif request.user.groups.filter(name="teacher").exists():
            return redirect("teacher")
        elif request.user.groups.filter(name="volunteer").exists():
            return redirect("volunteer")
        elif request.user.groups.filter(name="donor").exists():
            return redirect("donor")
        else:  # request.user.groups.filter(name = 'student').exists()
            return redirect("student")


@login_required
def change_pwd(request):
    if request.method == "POST":
        form = ChangePwdForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, "Your password was successfully updated!")
            request.user.userprofile.change_pwd = False
            request.user.userprofile.save()
            return redirect("home-home")
        else:
            messages.error(request, "Please correct the error below.")
    form = ChangePwdForm(request.user)
    return render(request, "home/change_pwd.html", {"form": form})


def logout_view(request):
    logout(request)
    return render(request, "home/logout.html")


def login(request):
    return redirect("login")


def register(request):
    return render(request, "home/register.html")


def landing_page(request):
    return render(request, "home/landing_page.html")


@login_required
def register_after_oauth(request):
    if request.method == "POST":
        if request.POST.get("role") == "student":
            student_group = Group.objects.get(name="student")
            student_group.user_set.add(request.user)
            return redirect("home-home")
        elif request.POST.get("role") == "volunteer":
            volunteer_group = Group.objects.get(name="volunteer")
            volunteer_group.user_set.add(request.user)
            return redirect("home-home")
        else:
            messages.error(request, "Please correct the error below.")
            return redirect("register_after_oauth")
    if DjangoUser.objects.filter(email=request.user.email).count() == 2:
        user_1 = DjangoUser.objects.filter(email=request.user.email)[0]
        user_2 = DjangoUser.objects.filter(email=request.user.email)[1]
        staff_group = Group.objects.get(name="staff")
        student_group = Group.objects.get(name="student")
        teacher_group = Group.objects.get(name="teacher")
        volunteer_group = Group.objects.get(name="volunteer")
        if user_1.groups.filter(name="staff"):
            staff_group.user_set.add(user_2)
        elif user_1.groups.filter(name="student"):
            student_group.user_set.add(user_2)
        elif user_1.groups.filter(name="teacher"):
            teacher_group.user_set.add(user_2)
        elif user_1.groups.filter(name="volunteer"):
            volunteer_group.user_set.add(user_2)
        elif user_2.groups.filter(name="staff"):
            staff_group.user_set.add(user_1)
        elif user_2.groups.filter(name="student"):
            student_group.user_set.add(user_1)
        elif user_2.groups.filter(name="teacher"):
            teacher_group.user_set.add(user_1)
        elif user_2.groups.filter(name="volunteer"):
            volunteer_group.user_set.add(user_1)
        return redirect("home-home")
    return render(request, "home/register_after_oauth.html")


def register_as_student(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            new_user = DjangoUser.objects.create_user(
                username=form.cleaned_data.get("username"),
                email=form.cleaned_data.get("email"),
                first_name=form.cleaned_data.get("first_name"),
                last_name=form.cleaned_data.get("last_name"),
                password=form.cleaned_data.get("password1"),
            )
            student_group = Group.objects.get(name="student")
            student_group.user_set.add(new_user)
            first_name = form.cleaned_data.get("first_name")
            messages.success(
                request,
                f"Student Account Successfully Created For {first_name}, please log in",
            )
            return redirect("login")
        return render(request, "home/register_as_student.html", {"form": form})
    else:
        form = UserRegisterForm()
        return render(request, "home/register_as_student.html", {"form": form})


def register_as_volunteer(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            new_user = DjangoUser.objects.create_user(
                username=form.cleaned_data.get("username"),
                email=form.cleaned_data.get("email"),
                first_name=form.cleaned_data.get("first_name"),
                last_name=form.cleaned_data.get("last_name"),
                password=form.cleaned_data.get("password1"),
            )
            volunteer_group = Group.objects.get(name="volunteer")
            volunteer_group.user_set.add(new_user)
            first_name = form.cleaned_data.get("first_name")
            messages.success(
                request,
                f"Volunteer Account Successfully Created For {first_name}, please log in",
            )
            return redirect("login")
        return render(request, "home/register_as_volunteer.html", {"form": form})
    else:
        form = UserRegisterForm()
        return render(request, "home/register_as_volunteer.html", {"form": form})


def register_as_donor(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            new_user = DjangoUser.objects.create_user(
                username=form.cleaned_data.get("username"),
                email=form.cleaned_data.get("email"),
                first_name=form.cleaned_data.get("first_name"),
                last_name=form.cleaned_data.get("last_name"),
                password=form.cleaned_data.get("password1"),
            )
            donor_group = Group.objects.get(name="donor")
            donor_group.user_set.add(new_user)
            first_name = form.cleaned_data.get("first_name")
            messages.success(
                request,
                f"Donor Account Successfully Created For {first_name}, please log in",
            )
            return redirect("login")
        return render(request, "home/register_as_donor.html", {"form": form})
    else:
        form = UserRegisterForm()
        return render(request, "home/register_as_donor.html", {"form": form})
