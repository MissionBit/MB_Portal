from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from django.contrib import messages

from home.forms import CreateStaffForm, CreateStudentForm, CreateTeacherForm, CreateVolunteerForm


@login_required
def staff(request):
    if not request.user.groups.filter(name='staff').exists():
        return HttpResponse('Unauthorized', status=401)
    return render(request, 'staff.html')


@login_required
def user_management(request):
    if not request.user.groups.filter(name='staff').exists():
        return HttpResponse('Unauthorized', status=401)
    return render(request, 'user_management.html')


@login_required
def contact_management(request):
    if not request.user.groups.filter(name='staff').exists():
        return HttpResponse('Unauthorized', status=401)
    return render(request, 'contact_management.html')


@login_required
def create_staff_user(request):
    if not request.user.groups.filter(name='staff').exists():
        return HttpResponse('Unauthorized', status=401)
    if request.method == 'POST':
        form = CreateStaffForm(request.POST)
        if form.is_valid():
            form.save()
            new_user = User.objects.create_user(
                username="%s.%s" % (form.cleaned_data.get('first_name'), form.cleaned_data.get('last_name')),
                email=form.cleaned_data.get('email'),
                first_name=form.cleaned_data.get('first_name'),
                last_name=form.cleaned_data.get('last_name'),
                password='missionbit'
                )
            new_user.userprofile.change_pwd = True
            new_user.save()
            staff_group = Group.objects.get(name='staff')
            staff_group.user_set.add(new_user)
            first_name = form.cleaned_data.get('first_name')
            messages.success(request, f'Staff Account Successfully Created For {first_name}')
            return redirect('staff')
        messages.error(request, 'Staff User NOT created, your form was not valid, please try again.')
        return redirect(request, 'staff')
    form = CreateStaffForm()
    return render(request, 'create_staff_user.html', {'form': form})


@login_required
def create_teacher_user(request):
    if not request.user.groups.filter(name='staff').exists():
        return HttpResponse('Unauthorized', status=401)
    if request.method == 'POST':
        form = CreateTeacherForm(request.POST)
        if form.is_valid():
            form.save()
            new_user = User.objects.create_user(
                username="%s.%s" % (form.cleaned_data.get('first_name'), form.cleaned_data.get('last_name')),
                email=form.cleaned_data.get('email'),
                first_name=form.cleaned_data.get('first_name'),
                last_name=form.cleaned_data.get('last_name'),
                password='missionbit'
                )
            new_user.userprofile.change_pwd = True
            new_user.save()
            teacher_group = Group.objects.get(name='teacher')
            teacher_group.user_set.add(new_user)
            first_name = form.cleaned_data.get('first_name')
            messages.success(request, f'Teacher Account Successfully Created For {first_name}')
            return redirect('staff')
    form = CreateTeacherForm()
    return render(request, 'create_teacher_user.html', {'form': form})


@login_required
def create_student_user(request):
    if not request.user.groups.filter(name='staff').exists():
        return HttpResponse('Unauthorized', status=401)
    if request.method == 'POST':
        form = CreateStudentForm(request.POST)
        if form.is_valid():
            form.save()
            new_user = User.objects.create_user(
                username="%s.%s" % (form.cleaned_data.get('first_name'), form.cleaned_data.get('last_name')),
                email=form.cleaned_data.get('email'),
                first_name=form.cleaned_data.get('first_name'),
                last_name=form.cleaned_data.get('last_name'),
                password='missionbit'
                )
            new_user.userprofile.change_pwd = True
            new_user.save()
            student_group = Group.objects.get(name='student')
            student_group.user_set.add(new_user)
            first_name = form.cleaned_data.get('first_name')
            messages.success(request, f'Student Account Successfully Created For {first_name}')
            return redirect('staff')
    form = CreateStudentForm()
    return render(request, 'create_student_user.html', {'form': form})


@login_required
def create_volunteer_user(request):
    if not request.user.groups.filter(name='staff').exists():
        return HttpResponse('Unauthorized', status=401)
    if request.method == 'POST':
        form = CreateVolunteerForm(request.POST)
        if form.is_valid():
            form.save()
            new_user = User.objects.create_user(
                username="%s.%s" % (form.cleaned_data.get('first_name'), form.cleaned_data.get('last_name')),
                email=form.cleaned_data.get('email'),
                first_name=form.cleaned_data.get('first_name'),
                last_name=form.cleaned_data.get('last_name'),
                password='missionbit'
                )
            new_user.userprofile.change_pwd = True
            new_user.save()
            volunteer_group = Group.objects.get(name='volunteer')
            volunteer_group.user_set.add(new_user)
            first_name = form.cleaned_data.get('first_name')
            messages.success(request, f'Student Account Successfully Created For {first_name}')
            return redirect('staff')
    form = CreateVolunteerForm()
    return render(request, 'create_volunteer_user.html', {'form': form})


@login_required
def create_classroom(request):
    if not request.user.groups.filter(name='staff').exists():
        return HttpResponse('Unauthorized', status=401)
    form = CreateClassroomForm()


@login_required
def my_account_staff(request):
    if not request.user.groups.filter(name='staff').exists():
        return HttpResponse('Unauthorized', status=401)
    return render(request, 'my_account_staff.html')

