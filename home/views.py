from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib.auth.models import Group
from django.contrib.auth.models import User as DjangoUser
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, ChangePwdForm
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash


@login_required
def home(request):
    """
    If the request's user already has a tag they are redirected to the correct page.  When a user
    first logs in they don't have a tag and they are directed based on the group they belong to with
    approximately the highest permission level.
    redirects ref:
    https://realpython.com/django-redirects/#django-redirects-a-super-simple-example
    """
    if request.user.userprofile.change_pwd:
        return redirect("change_pwd")
    else:
        if request.user.groups.all().count() == 0:
            return redirect("home-register_after_oauth")
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
    return render(request, "home/landing_page_MUI.html")


@login_required
def register_after_oauth(request):
    """
    This method catches a user who logs in with no groups, this may happen in two scenarios.
    Scenario 1: A user logs in with gmail who has never logged in before.  In that situation,
    the user is required to choose a group to complete registration, and is allowed to proceed.
    Scenario 2: A user logs in with gmail who has an account already, but has never logged in
    with gmail.  In that situation, our API auto-generates a new user account, creating a
    duplicate entry.  This method takes care of that by adding the new user to the old user's
    groups, and deleting the old user.
    """
    if request.method == "POST":
        if request.POST.get("role") == "student":
            student_group = Group.objects.get(name="student")
            student_group.user_set.add(request.user)
            return redirect("home-home")
        else:  # request.POST.get("role") == "volunteer":
            volunteer_group = Group.objects.get(name="volunteer")
            volunteer_group.user_set.add(request.user)
            return redirect("home-home")
    user_count = DjangoUser.objects.filter(email=request.user.email).count()
    if user_count >= 2:
        messages.error(
            request,
            "Error, multiple users with that email - please contact Mission Bit Staff",
        )
        logout(request)
        return render(request, "home/logout.html")
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
