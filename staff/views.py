from django.views.generic import DetailView, ListView
from django.shortcuts import render, redirect
from home.decorators import group_required
from home.forms import (
    CreateStaffForm,
    CreateClassroomForm,
    CreateTeacherForm,
    CreateVolunteerForm,
    CreateStudentForm,
    CreateClassOfferingForm,
    MakeAnnouncementForm,
    ChangeTeacherForm,
    AddVolunteersForm,
    AddStudentsForm,
)
from .staff_views_helper import *
from social_django.models import UserSocialAuth
from home.models.salesforce import Contact, ClassOffering, ClassEnrollment
from home.models.models import Classroom

@group_required("staff")
def staff(request):
    return render(request, "staff.html")


@group_required("staff")
def user_management(request):
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
                provider="google-oauth2"
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
                provider="google-oauth2"
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
                provider="google-oauth2"
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
                provider="google-oauth2"
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
            if form.instance.email_recipients:
                data = request.POST.copy()
                email_list = get_emails_from_form(data)
                email_announcement(request, form, email_list)
            form.save()
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
def my_account_staff(request):
    return render(request, "my_account_staff.html")


class ClassroomDetailView(DetailView):
    model = Classroom

    def get_forms(self):
        change_teacher_form = ChangeTeacherForm()
        add_volunteers_form = AddVolunteersForm()
        add_students_form = AddStudentsForm()
        return [change_teacher_form, add_volunteers_form, add_students_form]

    def get_context_data(self, **kwargs):
        context = super(ClassroomDetailView, self).get_context_data(**kwargs)
        forms = self.get_forms()
        context.update({
            "change_teacher_form": forms[0],
            "add_volunteers_form": forms[1],
            "add_students_form": forms[2]
        })

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


def change_classroom_teacher(request):
    teacher_contact = get_contact_by_user_id(request.POST["former_teacher"])
    class_offering = get_class_offering_by_id(request.POST["course_id"])
    new_teacher = get_contact_by_user_id(request.POST["teacher"])
    classroom = Classroom.objects.get(id=request.POST["course_id"])
    classroom.teacher_id = request.POST["teacher"]
    classroom.save()
    remove_enrollment(teacher_contact, class_offering)
    ClassEnrollment.objects.get_or_create(
        created_by=class_offering.created_by,
        contact=new_teacher,
        status="Enrolled",
        class_offering=class_offering,
    )
    class_offering.instructor = new_teacher
    class_offering.save()


def change_classroom_ta(request):
    ta_contact = get_contact_by_user_id(request.POST["former_ta"])
    class_offering = get_class_offering_by_id(request.POST["course_id"])
    new_ta = get_contact_by_user_id(request.POST["teacher"])
    classroom = Classroom.objects.get(id=request.POST["course_id"])
    classroom.teacher_assistant_id = request.POST["teacher"]
    classroom.save()
    remove_enrollment(ta_contact, class_offering)
    ClassEnrollment.objects.get_or_create(
        created_by=class_offering.created_by,
        contact=new_ta,
        status="Enrolled",
        class_offering=class_offering,
    )


def remove_volunteer(request):
    vol_contact = get_contact_by_user_id(request.POST["former_vol"])
    class_offering = get_class_offering_by_id(request.POST["course_id"])
    classroom = Classroom.objects.get(id=request.POST["course_id"])
    classroom.volunteers.remove(request.POST["former_vol"])
    remove_enrollment(vol_contact, class_offering)


def remove_student(request):
    student_contact = get_contact_by_user_id(request.POST["former_student"])
    class_offering = get_class_offering_by_id(request.POST["course_id"])
    classroom = Classroom.objects.get(id=request.POST["course_id"])
    classroom.students.remove(request.POST["former_student"])
    remove_enrollment(student_contact, class_offering)


def add_volunteers(request):
    form = AddVolunteersForm(request.POST)
    class_offering = get_class_offering_by_id(request.POST["course_id"])
    classroom = Classroom.objects.get(id=request.POST["course_id"])
    if form.is_valid():
        for volunteer in form.cleaned_data.get("volunteers"):
            vol_contact = get_contact_by_user_id(volunteer)
            ClassEnrollment.objects.create(
                created_by=class_offering.created_by,
                contact=vol_contact,
                status="Enrolled",
                class_offering=class_offering
            )
            classroom.volunteers.add(volunteer)


def add_students(request):
    form = AddStudentsForm(request.POST)
    class_offering = get_class_offering_by_id(request.POST["course_id"])
    classroom = Classroom.objects.get(id=request.POST["course_id"])
    if form.is_valid():
        for student in form.cleaned_data.get("students"):
            student_contact = get_contact_by_user_id(student)
            ClassEnrollment.objects.create(
                created_by=class_offering.created_by,
                contact=student_contact,
                status="Enrolled",
                class_offering=class_offering
            )
            classroom.students.add(student)


def remove_enrollment(contact, class_offering):
    old_enrollment = ClassEnrollment.objects.get(contact=contact, status="Enrolled", class_offering=class_offering)
    created_by = old_enrollment.created_by
    old_enrollment.delete()
    return created_by


def get_contact_by_user_id(id):
    return Contact.objects.get(client_id=UserProfile.objects.get(user_id=id).salesforce_id)


def get_class_offering_by_id(id):
    course_name = get_course_name_by_id(id)
    return ClassOffering.objects.get(name=course_name)


def get_course_name_by_id(id):
    return Classroom.objects.get(id=id).course
