from django.views.generic import DetailView, ListView
from django.contrib.auth.models import Group
from django.template.defaulttags import register
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
    AddForumForm,
    AddVolunteerForm,
    AddStudentForm
)
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
    announcements = Announcement.objects.filter(recipient_groups=Group.objects.get(name="staff").id)
    announcements = remove_dismissed_announcements(announcements, request.user)
    forms = Form.objects.filter(recipient_groups=Group.objects.get(name="staff").id)
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
    class_dict = {}
    classroom_list = Classroom.objects.all()
    for classroom in classroom_list:
        class_dict.update({classroom.course: get_class_member_dict(classroom)})
    return render(request, "classroom_management.html", {"classrooms": classroom_list,
                                                         "class_dicts": class_dict})


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
            setup_classroom(request, form)
            messages.success(
                request,
                f'Classroom {form.cleaned_data.get("course")} Successfully Created',
            )
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
            messages.add_message(
                request, messages.SUCCESS, "Successfully Added Class Offering"
            )
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
            user_list = get_users_from_form(form)
            email_list = [user.email for user in user_list]
            if form.instance.email_recipients:
                subject = form.cleaned_data.get("title")
                message = form.cleaned_data.get("announcement")
                email_announcement(request, subject, message, email_list)
            announcement = form.save()
            distribute_announcement(user_list, announcement)
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
            user_list = get_users_from_form(form)
            email_list = [user.email for user in user_list]
            if form.cleaned_data.get("email_recipients"):
                subject = form.cleaned_data.get("name")
                message = form.cleaned_data.get("description")
                email_posted_form(request, subject, message, email_list)
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
            classroom = Classroom.objects.get(id=request.POST.get("classroom"))
            classroom.forum_title = form.cleaned_data.get("forum_title")
            classroom.forum = form.cleaned_data.get("forum")
            classroom.save()
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
def classroom_detail(request):
    if request.method == "POST":
        if request.POST.get("swap_teacher"):
            form = ChangeTeacherForm(request.POST)
            if form.is_valid():
                change_classroom_lead(request.POST.get("fmr_teacher", None),
                                      form.cleaned_data.get("teacher").id,
                                      request.POST.get("course_id", None),
                                      "teacher")
                messages.add_message(request, messages.SUCCESS, "Teacher Successfully Changed")
                return redirect("staff")
            else:
                messages.add_message(request, messages.ERROR, "Invalid Form")  # Need to have fall through here
                return redirect("staff")
        if request.POST.get("swap_teacher_assistant"):
            form = ChangeTeacherForm(request.POST)
            if form.is_valid():
                change_classroom_lead(request.POST.get("fmr_teacher_assistant", None),
                                      form.cleaned_data.get("teacher").id,
                                      request.POST.get("course_id", None),
                                      "teacher_assistant")
                messages.add_message(request, messages.SUCCESS, "Teacher Assistant Successfully Changed")
                return redirect("staff")
            else:
                messages.add_message(request, messages.ERROR, "Invalid Form")  # Need to have fall through here
                return redirect("staff")
        if request.POST.get("remove_student"):  # Input Validation Needed
            remove_user_from_classroom(request.POST["fmr_student"], request.POST["course_id"])
            messages.add_message(request, messages.SUCCESS, "Student Successfully Removed From Class")
            return redirect("staff")
        if request.POST.get("remove_volunteer"):  # Input Validation Needed
            remove_user_from_classroom(request.POST["fmr_volunteer"], request.POST["course_id"])
            messages.add_message(request, messages.SUCCESS, "Volunteer Successfully Removed From Class")
            return redirect("staff")
        if request.POST.get("add_volunteer"):
            form = AddVolunteerForm(request.POST)
            if form.is_valid():
                add_user_to_classroom(form.cleaned_data.get("volunteer").id, request.POST["course_id"], "volunteer")
                messages.add_message(request, messages.SUCCESS, "Volunteer Added To Class")
                return redirect("staff")
            else:
                messages.add_message(request, messages.ERROR, "Invalid Form")  # Need to have fall through here
                return redirect("staff")
        if request.POST.get("add_student"):
            form = AddStudentForm(request.POST)
            if form.is_valid():
                add_user_to_classroom(form.cleaned_data.get("student").id, request.POST["course_id"], "student")
                messages.add_message(request, messages.SUCCESS, "Student Added To Class")
                return redirect("staff")
            else:
                messages.add_message(request, messages.ERROR, "Invalid Form")  # Need to have fall through here
                return redirect("staff")
    classroom = Classroom.objects.get(id=request.GET.get("course_id"))
    class_members = get_class_member_dict(classroom)
    return render(request, "classroom_detail.html", {"change_teacher_form": ChangeTeacherForm(),
                                                     "add_volunteer_form": AddVolunteerForm(),
                                                     "add_student_form": AddStudentForm(),
                                                     "classroom": classroom,
                                                     "class_members": class_members})


@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)


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
            "add_volunteers_form": AddVolunteerForm(),
            "add_students_form": AddStudentForm(),
        }

    def get_context_data(self, **kwargs):
        context = super(ClassroomDetailView, self).get_context_data(**kwargs)
        context.update(self.get_forms())
        return context

    def post(self, request, *args, **kwargs):
        if request.POST["change_who"] == "teacher":
            form = ChangeTeacherForm(request.POST)
            if form.is_valid():
                change_classroom_lead(request.POST["teacher"],
                                      form.cleaned_data.get("teacher").id,
                                      request.POST["course_id"],
                                      "teacher")
                messages.success(request, "Teacher Changed")
        elif request.POST["change_who"] == "ta":
            form = ChangeTeacherForm(request.POST)
            if form.is_valid():
                change_classroom_lead(request.POST["teacher"],
                                      form.cleaned_data.get("teacher").id,
                                      request.POST["course_id"],
                                      "teacher_assistant")
            messages.success(request, "TA Changed")
        elif request.POST["change_who"] == "remove_vol":
            remove_user_from_classroom(request.POST["former_vol"], request.POST["course_id"])
            messages.success(request, "Volunteer Removed")
        elif request.POST["change_who"] == "add_vols":
            form = AddVolunteerForm(request.POST)
            if form.is_valid():
                add_user_to_classroom(form.cleaned_data.get("volunteer").id, request.POST["course_id"], "volunteer")
            messages.success(request, "Volunteers Added")
        elif request.POST["change_who"] == "delete_student":
            remove_user_from_classroom(request.POST["former_student"], request.POST["course_id"])
            messages.success(request, "Student Removed")
        elif request.POST["change_who"] == "add_students":
            form = AddStudentForm(request.POST)
            if form.is_valid():
                add_user_to_classroom(form.cleaned_data.get("student").id, request.POST["course_id"], "student")
            messages.success(request, "Students Added")
        return redirect("classroom_management")


class ClassroomListView(ListView):
    model = Classroom
    template_name = "classroom_management.html"
    context_object_name = "classrooms"
