from django.views.generic import DetailView, ListView
from django.shortcuts import render, redirect
from home.decorators import group_required
from django.http import HttpResponse, Http404
from home.forms import (
    CreateStaffForm,
    CreateClassroomForm,
    CreateTeacherForm,
    CreateVolunteerForm,
    CreateStudentForm,
    CreateClassOfferingForm,
    MakeAnnouncementForm,
    ChangeTeacherForm,
    PostFormForm,
    CreateEsignForm,
    CollectForms,
    NotifyUnsubmittedUsersForm,
    AddCurriculumForm,
    AddForumForm
)
from missionbit.settings import GROUP_IDS
from .staff_views_helper import *
from attendance.views import get_date_from_template_returned_string
from social_django.models import UserSocialAuth
from home.models.models import Classroom, Form, Esign, Notification, Announcement
import os


@group_required("staff")
def staff(request):
    if request.method == "POST":
        if request.POST.get("dismiss_announcement") == "true":
            mark_announcement_dismissed(Announcement.objects.get(id=request.POST.get("announcement")), request.user)
            return redirect("staff")
        elif request.POST.get("acknowledge_notification") == "true":
            mark_notification_acknowledged(Notification.objects.get(id=request.POST.get("notification")))
            return redirect("staff")
    announcements = Announcement.objects.filter(recipient_groups=GROUP_IDS.get("staff"))
    announcements = remove_dismissed_announcements(announcements, request.user)
    forms = Form.objects.filter(recipient_groups=GROUP_IDS.get("staff"))
    forms = remove_submitted_forms(forms, request.user)
    notifications = Notification.objects.filter(user_id=request.user.id, acknowledged=False)
    return render(request, "staff.html", {"announcements": announcements,
                                          "forms": forms,
                                          "notifications": notifications})


@group_required("staff")
def user_management(request):
    names = DjangoUser.objects.all()
    context = {"names": names}
    return render(request, "user_management.html")


@group_required("staff")
def classroom_management(request):
    all_classrooms = {}
    for classroom in Classroom.objects.all():
        teacher_user = DjangoUser.objects.get(id=classroom.teacher_id)
        teacher_assistant_user = DjangoUser.objects.get(
            id=classroom.teacher_assistant_id
        )
        student_list = add_students_to_student_dict(classroom)
        volunteer_list = add_volunteers_to_volunteer_dict(classroom)
        class_dict = {
            "id": classroom.id,
            "teacher": "%s %s" % (teacher_user.first_name, teacher_user.last_name),
            "teacher_assistant": "%s %s"
            % (teacher_assistant_user.first_name, teacher_assistant_user.last_name),
            "student_list": student_list,
            "volunteer_list": volunteer_list,
        }
        all_classrooms[str(classroom.course)] = class_dict

    return render(request, "classroom_management.html", {"classrooms": all_classrooms})


@group_required("staff")
def create_staff_user(request):
    if request.method == "POST":
        form = CreateStaffForm(request.POST)
        if form.is_valid():
            form.save()
            random_password = DjangoUser.objects.make_random_password()
            new_user = create_user_with_profile(form, random_password)
            email = form.cleaned_data.get("email")
            staff_group = Group.objects.get(name="staff")
            staff_group.user_set.add(new_user)
            UserSocialAuth.objects.create(
                uid=form.cleaned_data.get("email"),
                user_id=new_user.userprofile.user_id,
                provider="google-oauth2",
            )
            first_name = form.cleaned_data.get("first_name")
            messages.success(
                request, f"Staff Account Successfully Created For {first_name}"
            )
            email_new_user(
                request, email, first_name, "staff", new_user.username, random_password
            )
            return redirect("staff")
        else:
            messages.error(
                request,
                "Staff User NOT created, your form was not valid, please try again.",
            )
            return redirect("staff")
    form = CreateStaffForm()
    return render(request, "create_staff_user.html", {"form": form})


@group_required("staff")
def create_teacher_user(request):
    if request.method == "POST":
        form = CreateTeacherForm(request.POST)
        if form.is_valid():
            form.save()
            random_password = DjangoUser.objects.make_random_password()
            new_user = create_user_with_profile(form, random_password)
            email = form.cleaned_data.get("email")
            teacher_group = Group.objects.get(name="teacher")
            teacher_group.user_set.add(new_user)
            UserSocialAuth.objects.create(
                uid=form.cleaned_data.get("email"),
                user_id=new_user.userprofile.user_id,
                provider="google-oauth2",
            )
            first_name = form.cleaned_data.get("first_name")
            messages.success(
                request, f"Teacher Account Successfully Created For {first_name}"
            )
            email_new_user(
                request,
                email,
                first_name,
                "teacher",
                new_user.username,
                random_password,
            )
            return redirect("staff")
        else:
            messages.error(
                request,
                "Teacher User NOT created, your form was not valid, please try again.",
            )
            return redirect("staff")
    form = CreateTeacherForm()
    return render(request, "create_teacher_user.html", {"form": form})


@group_required("staff")
def create_student_user(request):
    if request.method == "POST":
        form = CreateStudentForm(request.POST)
        if form.is_valid():
            form.save()
            random_password = DjangoUser.objects.make_random_password()
            new_user = create_user_with_profile(form, random_password)
            email = form.cleaned_data.get("email")
            student_group = Group.objects.get(name="student")
            student_group.user_set.add(new_user)
            UserSocialAuth.objects.create(
                uid=form.cleaned_data.get("email"),
                user_id=new_user.userprofile.user_id,
                provider="google-oauth2",
            )
            first_name = form.cleaned_data.get("first_name")
            messages.success(
                request, f"Student Account Successfully Created For {first_name}"
            )
            email_new_user(
                request,
                email,
                first_name,
                "student",
                new_user.username,
                random_password,
            )
            return redirect("staff")
        else:
            messages.error(
                request,
                "Student User NOT created, your form was not valid, please try again.",
            )
            return redirect("staff")
    form = CreateStudentForm()
    return render(request, "create_student_user.html", {"form": form})


@group_required("staff")
def create_volunteer_user(request):
    if request.method == "POST":
        form = CreateVolunteerForm(request.POST)
        if form.is_valid():
            form.save()
            random_password = DjangoUser.objects.make_random_password()
            new_user = create_user_with_profile(form, random_password)
            email = form.cleaned_data.get("email")
            volunteer_group = Group.objects.get(name="volunteer")
            volunteer_group.user_set.add(new_user)
            UserSocialAuth.objects.create(
                uid=form.cleaned_data.get("email"),
                user_id=new_user.userprofile.user_id,
                provider="google-oauth2",
            )
            first_name = form.cleaned_data.get("first_name")
            messages.success(
                request, f"Volunteer Account Successfully Created For {first_name}"
            )
            email_new_user(
                request,
                email,
                first_name,
                "volunteer",
                new_user.username,
                random_password,
            )
            return redirect("staff")
        else:
            messages.error(
                request,
                "Volunteer User NOT created, your form was not valid, please try again.",
            )
            return redirect("staff")
    form = CreateVolunteerForm()
    return render(request, "create_volunteer_user.html", {"form": form})


@group_required("staff")
def create_classroom(request):
    if request.method == "POST":
        form = CreateClassroomForm(request.POST)
        if form.is_valid():
            classroom = setup_classroom_teachers(request, form)
            add_volunteers_and_students_to_classroom(request, form, classroom)
            generate_classroom_sessions_and_attendance(classroom)
            messages.success(
                request,
                f'Classroom {form.cleaned_data.get("course")} Successfully Created',
            )
            classroom.save()
            return redirect("staff")
        else:
            messages.error(
                request,
                "Classroom NOT created, your form was not valid, please try again.",
            )
            return redirect("staff")
    form = CreateClassroomForm()
    return render(request, "create_classroom.html", {"form": form})


@group_required("staff")
def create_class_offering(request):
    if request.method == "POST":
        form = CreateClassOfferingForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("staff")
        else:
            messages.error(
                request,
                "Class offering NOT created, your form was not valid, please try again.",
            )
            return redirect("staff")
    form = CreateClassOfferingForm()
    return render(request, "create_class_offering.html", {"form": form})


@group_required("staff")
def make_announcement(request):
    if request.method == "POST":
        form = MakeAnnouncementForm(request.POST)
        if form.is_valid():
            form.instance.created_by = DjangoUser.objects.get(id=request.user.id)
            data = request.POST.copy()
            user_dict = get_users_and_emails_from_form(data)
            if form.instance.email_recipients:
                email_announcement(request, form, user_dict.get("email_list"))
            announcement = form.save()
            distribute_announcement(user_dict.get("user_list"), announcement)
            messages.add_message(
                request, messages.SUCCESS, "Successfully Made Announcement"
            )
            return redirect("staff")
        else:
            messages.error(
                request,
                "Announcement NOT made, your announcement form was not valid, please try again.",
            )
            return redirect("staff")
    form = MakeAnnouncementForm(
        initial={"created_by": DjangoUser.objects.get(id=request.user.id)}
    )
    return render(request, "make_announcement.html", {"form": form})


@group_required("staff")
def post_form(request):
    if request.method == "POST":
        form = PostFormForm(request.POST, request.FILES)
        if form.is_valid():
            posted_form = Form(
                name=form.cleaned_data.get("name"),
                description=form.cleaned_data.get("description"),
                form=request.FILES["form"],
                created_by=DjangoUser.objects.get(id=request.user.id),
            )
            if form.cleaned_data.get("esign") is not None:
                posted_form.esign = form.cleaned_data.get("esign")
            posted_form.save()
            posted_form.recipient_groups.set(form.cleaned_data.get("recipient_groups"))
            posted_form.recipient_classrooms.set(
                form.cleaned_data.get("recipient_classrooms")
            )
            messages.add_message(request, messages.SUCCESS, "Successfully Posted Form")
            data = request.POST.copy()
            user_dict = get_users_and_emails_from_form(data)
            if form.cleaned_data.get("email_recipients"):
                email_posted_form(request, form, user_dict.get("email_list"))
            distribute_forms(request, posted_form, form)
            return redirect("staff")
        else:
            messages.error(
                request,
                "Form NOT made, your form form was not valid, please try again.",
            )
            return redirect("staff")
    form = PostFormForm(
        initial={"created_by": DjangoUser.objects.get(id=request.user.id)}
    )
    return render(request, "post_form.html", {"form": form})


@group_required("staff")
def form_overview(request):
    if request.method == "POST":
        form = CollectForms(request.POST)
        if form.is_valid():
            form_id = Form.objects.get(name=request.POST.get("form_name"))
            form_distribution = FormDistribution.objects.get(user_id=request.POST.get("user_id"), form_id=form_id)
            form_distribution.submitted = form.cleaned_data.get("submitted")
            form_distribution.save()
        return redirect("form_overview")
    outstanding_form_dict = get_outstanding_forms()
    form = CollectForms()
    return render(request, "form_overview.html", {"outstanding_form_dict": outstanding_form_dict,
                                                  "form": form})


@group_required("staff")
def notify_unsubmitted_users(request):
    if request.method == "POST":
        form = NotifyUnsubmittedUsersForm(request.POST)
        if form.is_valid():
            form_id = Form.objects.get(name=request.POST.get("notify_about")).id
            form_distributions = FormDistribution.objects.filter(form_id=form_id, submitted=False)
            for form_dist in form_distributions:
                create_form_notification(request, form, form_dist.user_id)
            if form.cleaned_data.get("email_recipients"):
                email_list = get_emails_from_form_distributions(form_distributions)
                email_form_notification(request, form, email_list)
            messages.add_message(request, messages.SUCCESS, "Successfully Notified Users")
            return redirect("staff")
    form = NotifyUnsubmittedUsersForm()
    notify_about = request.GET.get("notify_unsubmitted_users")
    return render(request, "notify_unsubmitted_users.html", {"form": form,
                                                             "notify_about": notify_about})


@group_required("staff")
def create_form_notification(request, form, user_id):
    notification = Notification(
        subject=form.cleaned_data.get("subject"),
        notification=form.cleaned_data.get("notification"),
        email_recipients=form.cleaned_data.get("email_recipients"),
        created_by=DjangoUser.objects.get(id=request.user.id),
        form_id=Form.objects.get(name=request.POST.get("notify_about")).id,
        user_id=user_id
    )
    notification.save()


@group_required("staff")
def communication_manager(request):
    if request.method == "POST":
        if request.POST.get("delete_announcement"):
            Announcement.objects.get(id=request.POST.get("announcement_id")).delete()
        elif request.POST.get("delete_notification"):
            Notification.objects.get(id=request.POST.get("notification_id")).delete()
        elif request.POST.get("delete_form"):
            Form.objects.get(id=request.POST.get("form_id")).delete()
        messages.add_message(request, messages.SUCCESS, "Deleted Successfully")
        return redirect("staff")
    announcements = Announcement.objects.all()
    notifications = Notification.objects.all()
    forms = Form.objects.all()
    return render(request, "communication_manager.html", {"announcements": announcements,
                                                          "notifications": notifications,
                                                          "forms": forms})


@group_required("staff")
def create_esign(request):
    if request.method == "POST":
        form = CreateEsignForm(request.POST)
        if form.is_valid():
            esign = Esign(
                name=form.cleaned_data.get("name"),
                template=form.cleaned_data.get("link"),
                created_by=DjangoUser.objects.get(id=request.user.id)
            )
            esign.save()
        messages.add_message(request, messages.SUCCESS, "Esign Created Successfully")
        return redirect("staff")
    form = CreateEsignForm(
        initial={"created_by": DjangoUser.objects.get(id=request.user.id)}
    )
    return render(request, "create_esign.html", {"form": form})


@group_required("staff")
def add_forum(request):
    if request.method == "POST":
        form = AddForumForm(request.POST)
        if form.is_valid():
            print("valid form")
            classroom = Classroom.objects.get(id=request.POST.get("classroom"))
            classroom.forum_title = form.cleaned_data.get("forum_title")
            classroom.forum = form.cleaned_data.get("forum")
            classroom.save()
            print("yay??!??")
            return redirect("staff")
    classroom = Classroom.objects.get(id=request.GET.get("classroom"))
    form = AddForumForm()
    return render(request, "add_forum.html", {"form": form,
                                              "classroom": classroom})


@group_required("staff")
def my_account_staff(request):
    return render(request, "my_account_staff.html")


@group_required("staff")
def curriculum(request):
    classroom = Classroom.objects.get(id=request.GET.get("classroom_id"))
    sessions = Session.objects.filter(classroom_id=classroom.id).order_by("date")
    return render(request, "curriculum.html", {"sessions": sessions,
                                               "classroom": classroom})


@group_required("staff")
def modify_session(request):
    if request.method == "POST":
        form = AddCurriculumForm(request.POST, request.FILES)
        if form.is_valid():
            update_session(request, form)
    form = AddCurriculumForm()
    date = request.GET.get("date")
    classroom = Classroom.objects.get(id=request.GET.get("classroom"))
    session = Session.objects.get(classroom_id=request.GET.get("classroom"),
                                  date=get_date_from_template_returned_string(request.GET.get("date")))
    return render(request, "modify_session.html", {"form": form,
                                                   "date": date,
                                                   "classroom": classroom,
                                                   "session": session})


@group_required("staff")
def download_form_staff(request):
    path = request.GET.get("path")
    file_path = os.path.join(path)
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="pdf/text")
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
            return response
    raise Http404


class ClassroomDetailView(DetailView):
    model = Classroom

    def get_forms(self):
        return {
            "change_teacher_form": ChangeTeacherForm(),
            "add_volunteers_form": AddVolunteersForm(),
            "add_students_form": AddStudentsForm(),
        }

    def get_context_data(self, **kwargs):
        context = super(ClassroomDetailView, self).get_context_data(**kwargs)
        context.update(self.get_forms())
        return context

    def post(self, request, *args, **kwargs):
        if request.POST["change_who"] == "teacher":
            change_classroom_teacher(request)
            messages.success(request, "Teacher Changed")
        elif request.POST["change_who"] == "ta":
            change_classroom_ta(request)
            messages.success(request, "TA Changed")
        elif request.POST["change_who"] == "remove_vol":
            remove_volunteer(request)
            messages.success(request, "Volunteer Removed")
        elif request.POST["change_who"] == "add_vols":
            add_volunteers(request)
            messages.success(request, "Volunteers Added")
        elif request.POST["change_who"] == "delete_student":
            remove_student(request)
            messages.success(request, "Student Removed")
        elif request.POST["change_who"] == "add_students":
            add_students(request)
            messages.success(request, "Students Added")
        return redirect("classroom_management")


class ClassroomListView(ListView):
    model = Classroom
    template_name = "classroom_management.html"
    context_object_name = "classrooms"
