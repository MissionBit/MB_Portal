from django.contrib.auth.models import User as DjangoUser
from django.contrib.auth.models import Group
from home.models.salesforce import ClassEnrollment, Contact, ClassOffering
from home.models.models import UserProfile, Classroom, Attendance, Session
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from django.contrib import messages
from home.forms import AddVolunteersForm, AddStudentsForm
from datetime import timedelta


def create_user_with_profile(form, random_password):
    new_user = DjangoUser.objects.create_user(
        username="%s.%s"
        % (form.cleaned_data.get("first_name"), form.cleaned_data.get("last_name")),
        email=form.cleaned_data.get("email"),
        first_name=form.cleaned_data.get("first_name"),
        last_name=form.cleaned_data.get("last_name"),
        password=random_password,
    )
    new_user = parse_new_user(new_user, form)
    new_user.save()
    return new_user


def parse_new_user(new_user, form):
    birthdate = str(form.cleaned_data.get("birthdate")).replace(r"/", "")
    birthdate_year = birthdate[0:4]
    birthdate_m = birthdate[8:]
    birthdate_d = birthdate[5:7]
    new_user.userprofile.change_pwd = True
    new_user.userprofile.salesforce_id = "%s%s%s%s%s" % (
        form.cleaned_data.get("first_name")[:3].lower(),
        form.cleaned_data.get("last_name")[:3].lower(),
        birthdate_year,
        birthdate_d,
        birthdate_m,
    )
    new_user.userprofile.date_of_birth = "%s-%s-%s" % (
        birthdate_year,
        birthdate_d,
        birthdate_m,
    )
    return new_user


def enroll_in_class(form, user):
    ClassEnrollment.objects.get_or_create(
        name=form.cleaned_data.get("course"),
        created_by=form.cleaned_data.get("created_by"),
        contact=user,
        status="Enrolled",
        class_offering=form.cleaned_data.get("course"),
    )


def setup_classroom_teachers(request, form):
    classroom = Classroom.objects.create(
        teacher_id=UserProfile.objects.get(salesforce_id=form.cleaned_data.get("teacher").client_id.lower()).user_id,
        teacher_assistant_id=UserProfile.objects.get(salesforce_id=form.cleaned_data.get("teacher_assistant").client_id.lower()).user_id,
        course=form.cleaned_data.get("course").name,
    )
    teacher_email_list = [
        DjangoUser.objects.get(id=classroom.teacher_id).email,
        DjangoUser.objects.get(id=classroom.teacher_assistant_id).email,
    ]
    enroll_in_class(form, form.cleaned_data.get("teacher"))
    enroll_in_class(form, form.cleaned_data.get("teacher_assistant"))
    email_classroom(request, teacher_email_list, classroom.course)
    return classroom


def add_volunteers_and_students_to_classroom(request, form, classroom):
    email_list = []
    for volunteer in form.cleaned_data.get("volunteers"):
        enroll_in_class(form, volunteer)
        django_user = UserProfile.objects.get(salesforce_id=volunteer.client_id.lower()).user_id
        classroom.volunteers.add(django_user)
        email_list.append(DjangoUser.objects.get(id=django_user).email)
    for student in form.cleaned_data.get("students"):
        enroll_in_class(form, student)
        django_user = UserProfile.objects.get(salesforce_id=student.client_id.lower()).user_id
        classroom.students.add(django_user)
        email_list.append(DjangoUser.objects.get(id=django_user).email)
    email_classroom(request, email_list, classroom.course)


def email_new_user(request, email, first_name, account_type, username, password):
    subject = "%s - Your new %s account has been set up" % (first_name, account_type)
    msg_html = render_to_string(
        "email_templates/new_user_email.html",
        {
            "first_name": first_name,
            "email": email,
            "username": username,
            "password": password,
            "account_type": account_type,
        },
    )
    from_user = settings.EMAIL_HOST_USER
    send_mail(
        subject=subject,
        message=strip_tags(msg_html),
        from_email=from_user,
        recipient_list=["tyler.iams@gmail.com"],  # Will replace with email
        html_message=msg_html,
    )
    messages.add_message(request, messages.SUCCESS, "Email sent successfully")


def email_classroom(request, email_list, classroom_name):
    subject = "Your Mission Bit %s Classroom Has Been Created" % classroom_name
    msg_html = render_to_string(
        "email_templates/new_classroom_email.html", {"classroom_name": classroom_name}
    )
    from_user = settings.EMAIL_HOST_USER
    recipient_list = [
        "tyler.iams@gmail.com",
        "iams.sophia@gmail.com",
    ]  # Will replace with email_list
    send_mail(
        subject=subject,
        message=strip_tags(msg_html),
        from_email=from_user,
        recipient_list=recipient_list,
        html_message=msg_html,
    )
    messages.add_message(request, messages.SUCCESS, "Email sent successfully")


def get_emails_from_form(form):
    email_list = []
    groups = form.getlist('recipient_groups')
    for group in groups:
        group_name = Group.objects.get(id=group)
        users = DjangoUser.objects.filter(groups__name=group_name)
        for user in users:
            email_list.append(user.email)
    classrooms = form.getlist('recipient_classrooms')
    for classroom in classrooms:
        classroom_object = Classroom.objects.get(id=classroom)
        teacher = DjangoUser.objects.get(id=classroom_object.teacher_id).email
        email_list.append(teacher.email)
        teacher_assistant = DjangoUser.objects.get(id=classroom_object.teacher_assistant_id).email
        email_list.append(teacher_assistant.email)
        students = DjangoUser.objects.filter(classroom_students__course=classroom_object.course)
        volunteers = DjangoUser.objects.filter(classroom_volunteers__course=classroom_object.course)
        for student in students:
            email_list.append(student.email)
        for volunteer in volunteers:
            email_list.append(volunteer.email)
    return email_list


def email_announcement(request, form, email_list):
    subject = form.instance.title
    msg_html = render_to_string(
        "email_templates/announcement_email.html", {"subject": form.instance.title,
                                                    "message": form.instance.announcement,
                                                    "from": form.instance.created_by}
    )
    from_user = settings.EMAIL_HOST_USER
    recipient_list = [
        "tyler.iams@gmail.com",
        "iams.sophia@gmail.com",
    ]  # Will replace with email_list
    send_mail(
        subject=subject,
        message=strip_tags(msg_html),
        from_email=from_user,
        recipient_list=recipient_list,
        html_message=msg_html,
    )
    messages.add_message(request, messages.SUCCESS, "Recipients Successfully Emailed")


def add_students_to_student_dict(classroom):
    student_dict = {}
    for x, student in enumerate(classroom.students.all()):
        student_user = DjangoUser.objects.get(id=student.id)
        student_dict["student%s" % x] = "%s %s" % (
            student_user.first_name,
            student_user.last_name,
        )
    return student_dict


def add_volunteers_to_volunteer_dict(classroom):
    volunteer_dict = {}
    for x, volunteer in enumerate(classroom.volunteers.all()):
        volunteer_user = DjangoUser.objects.get(id=volunteer.id)
        volunteer_dict["volunteer%s" % x] = "%s %s" % (
            volunteer_user.first_name,
            volunteer_user.last_name,
        )
    return volunteer_dict


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


def sync_attendance_with_salesforce_class_offerings():
    """
    This method is fluid; in its current state it will duplicate entries
    in your postgres attendance database if you've already got attendance data!
    Only use if you don't have attendance data but do have Classroom
    data.
    """
    for classoffering in ClassOffering.objects.all():
        dates = class_offering_meeting_dates(classoffering)
        classroom = Classroom.objects.get(course=classoffering.name)
        for day in dates:
            session = Session.objects.create()
            for student in classroom.students.all():
                Attendance.objects.create(
                    student_id=student.id,
                    session_id=session.id,
                    classroom_id=classroom.id,
                    date=day
                )


def class_offering_meeting_dates(class_offering):
    int_days = get_integer_days(class_offering)
    class_range = class_offering.end_date - class_offering.start_date
    dates = []
    for i in range(class_range.days + 1):
        the_date = class_offering.start_date + timedelta(days=i)
        if the_date.weekday() in int_days:
            dates.append(the_date)
    return dates


def get_integer_days(class_offering):
    if class_offering.meeting_days == "M-F":
        return [0, 1, 2, 3, 4]
    elif class_offering.meeting_days == "M/W":
        return [0, 2]
    elif class_offering.meeting_days == "T/R":
        return [1, 3]
