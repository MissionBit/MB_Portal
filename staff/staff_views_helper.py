from django.contrib.auth.models import User as DjangoUser
from django.contrib.auth.models import Group
from django.shortcuts import render
from home.models.salesforce import ClassEnrollment, Contact, ClassOffering
from home.models.models import (
    Announcement,
    UserProfile,
    Classroom,
    ClassroomMembership,
    Attendance,
    Session,
    FormDistribution,
    Form,
    AnnouncementDistribution,
)
from social_django.models import UserSocialAuth
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from django.contrib import messages
from datetime import timedelta, datetime
from salesforce.dbapi.exceptions import *


def create_user_with_profile(form, random_password):
    username = validate_username(
        "%s.%s"
        % (form.cleaned_data.get("first_name"), form.cleaned_data.get("last_name"))
    )
    new_user = DjangoUser.objects.create_user(
        username=username,
        email=form.cleaned_data.get("email"),
        first_name=form.cleaned_data.get("first_name"),
        last_name=form.cleaned_data.get("last_name"),
        password=random_password,
    )
    new_user = parse_new_user(new_user, form)
    new_user.save()
    return new_user


def validate_username(username):
    i = 1
    while DjangoUser.objects.filter(username=username).count() > 0:
        username = username + str(i)
        i += 1
    return username


def parse_new_user(new_user, form):
    birthdate = form.cleaned_data.get("birthdate")
    if birthdate is None:
        birthdate = datetime.strptime("January 1, 1901", "%B %d, %Y")
    new_user.userprofile.change_pwd = True
    new_user.userprofile.salesforce_id = "%s%s%s%s%s" % (
        form.cleaned_data.get("first_name")[:3].lower(),
        form.cleaned_data.get("last_name")[:3].lower(),
        "%04d" % birthdate.year,
        "%02d" % birthdate.month,
        "%02d" % birthdate.day,
    )
    new_user.userprofile.date_of_birth = birthdate
    return new_user


def save_user_to_salesforce(request, form):
    try:
        form.save()
    except SalesforceError:
        messages.error(request, "Error Saving User To Salesforce Database.")
        return render(request, "create_staff_user.html", {"form": form})


def create_mission_bit_user(request, form, group):
    random_password = DjangoUser.objects.make_random_password()
    new_user = create_user_with_profile(form, random_password)
    email = form.cleaned_data.get("email")
    student_group = Group.objects.get(name=group)
    student_group.user_set.add(new_user)
    UserSocialAuth.objects.create(
        uid=form.cleaned_data.get("email"),
        user_id=new_user.userprofile.user_id,
        provider="google-oauth2",
    )
    first_name = form.cleaned_data.get("first_name")
    messages.success(request, f"Student Account Successfully Created For {first_name}")
    email_new_user(
        request, email, first_name, group, new_user.username, random_password
    )


def enroll_in_class(form, contact):
    ClassEnrollment.objects.get_or_create(
        name=form.cleaned_data.get("course"),
        created_by=form.cleaned_data.get("created_by"),
        contact=contact,
        status="Enrolled",
        class_offering=form.cleaned_data.get("course"),
    )


def setup_classroom(request, form):
    email_list = []
    teacher = get_django_user_from_contact(form.cleaned_data.get("teacher"))
    teacher_assistant = get_django_user_from_contact(
        form.cleaned_data.get("teacher_assistant")
    )
    email_list.append(teacher.email)
    email_list.append(teacher_assistant.email)
    classroom = Classroom.objects.create(course=form.cleaned_data.get("course").name)
    create_classroom_membership(teacher, classroom, "teacher")
    create_classroom_membership(teacher_assistant, classroom, "teacher_assistant")
    enroll_in_class(form, form.cleaned_data.get("teacher"))
    enroll_in_class(form, form.cleaned_data.get("teacher_assistant"))
    for volunteer in form.cleaned_data.get("volunteers"):
        enroll_in_class(form, volunteer)
        django_volunteer = get_django_user_from_contact(volunteer)
        create_classroom_membership(django_volunteer, classroom, "volunteer")
        email_list.append(django_volunteer.email)
    for student in form.cleaned_data.get("students"):
        enroll_in_class(form, student)
        django_student = get_django_user_from_contact(student)
        create_classroom_membership(django_student, classroom, "student")
        email_list.append(django_student.email)
    generate_classroom_sessions_and_attendance(classroom)
    email_classroom(request, email_list, classroom.course)


def get_django_user_from_contact(contact):
    return DjangoUser.objects.get(
        id=UserProfile.objects.get(salesforce_id=contact.client_id.lower()).user_id
    )


def retrieve_userprofile_from_form(form, name_string):
    return UserProfile.objects.get(
        salesforce_id=form.cleaned_data.get(name_string).client_id.lower()
    )


def create_classroom_membership(django_user_member, classroom, membership_type):
    cm = ClassroomMembership(
        member=django_user_member, classroom=classroom, membership_type=membership_type
    )
    cm.save()


def generate_classroom_sessions_and_attendance(classroom):
    classroom.attendance_summary = {
        "attendance_statistic": get_course_attendance_statistic(classroom.id)
    }
    classroom.save()
    class_offering = ClassOffering.objects.get(name=classroom.course)
    dates = class_offering_meeting_dates(class_offering)
    sessions = [Session(classroom_id=classroom.id, date=day) for day in dates]
    Session.objects.bulk_create(sessions)
    classroom_students = get_users_of_type_from_classroom(classroom, "student")
    attendances = [
        Attendance(
            student_id=student.id,
            session_id=session.id,
            classroom_id=classroom.id,
            date=session.date,
        )
        for student in classroom_students
        for session in sessions
    ]
    Attendance.objects.bulk_create(attendances)


def get_classroom_sessions(classroom):
    return Session.objects.filter(classroom=classroom)


def get_users_of_type_from_classroom(classroom, type):
    return DjangoUser.objects.filter(
        classroom=classroom, classroom_member__membership_type=type
    )  # Handle Empty Set Case


def get_teacher_from_classroom(classroom):
    return DjangoUser.objects.get(
        classroom=classroom, classroom_member__membership_type="teacher"
    )  # Handle a multiple values returned exception


def get_teacher_assistant_from_classroom(classroom):
    return DjangoUser.objects.get(
        classroom=classroom, classroom_member__membership_type="teacher_assistant"
    )  # Handle a multiple values returned exception


def get_classroom_by_django_user(django_user):
    try:
        return Classroom.objects.get(membership_classroom__member=django_user)
    except Classroom.DoesNotExist:
        return None


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


def get_users_from_form(form):
    group_users = DjangoUser.objects.filter(
        groups__name__in=list(form.cleaned_data.get("recipient_groups"))
    )
    classroom_users = DjangoUser.objects.filter(
        classroom__in=list(form.cleaned_data.get("recipient_classrooms"))
    )
    print("--------------------------")
    print("group users | classroom users: ", (group_users | classroom_users).__len__())
    print("--------------------------")
    print("group users | classroom users distinct: ", (group_users | classroom_users).distinct().__len__())
    print("--------------------------")
    return (classroom_users | group_users).distinct()


def get_emails_from_form_distributions(form_distributions):
    return DjangoUser.objects.filter(
        email__in=[form_dist.user.email for form_dist in form_distributions]
    )


def email_announcement(request, subject, message, email_list):
    msg_html = render_to_string(
        "email_templates/announcement_email.html",
        {"subject": subject, "message": message, "from": request.user},
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


def bulk_distribute_announcement(user_list, announcement):
    announcement_distributions = [
        AnnouncementDistribution(
            user_id=user.id, announcement_id=announcement.id, dismissed=False
        )
        for user in user_list
    ]
    AnnouncementDistribution.objects.bulk_create(announcement_distributions)


def email_posted_form(request, esign, subject, message, email_list):
    msg_html = render_to_string(
        "email_templates/post_form_email.html",
        {
            "subject": subject,
            "message": message,
            "from": DjangoUser.objects.get(id=request.user.id),
            "esign_link": esign,
        },
    )
    text_content = "Please view your new form (attached)"
    recipient_list = [
        "tyler.iams@gmail.com",
        "iams.sophia@gmail.com",
    ]  # Will replace with email_list
    email = EmailMultiAlternatives(
        subject, text_content, settings.EMAIL_HOST_USER, recipient_list
    )
    email.attach_alternative(msg_html, "text/html")
    email.attach_file(
        "%s%s" % ("documents/", str(request.FILES["form"]).replace(" ", "_"))
    )
    email.send()
    messages.add_message(request, messages.SUCCESS, "Recipients Successfully Emailed")


def change_classroom_lead(
    former_leader_user_id, new_leader_user_id, course_id, leader_type
):
    class_offering = get_class_offering_by_id(course_id)
    new_lead_contact = get_contact_by_user_id(new_leader_user_id)
    classroom = Classroom.objects.get(id=course_id)
    remove_user_from_classroom(former_leader_user_id, course_id)
    create_classroom_membership(
        DjangoUser.objects.get(id=new_leader_user_id), classroom, leader_type
    )
    ClassEnrollment.objects.get_or_create(
        created_by=class_offering.created_by,
        contact=new_lead_contact,
        status="Enrolled",
        class_offering=class_offering,
    )
    if leader_type is "teacher":
        class_offering.instructor = new_lead_contact
        class_offering.save()


def remove_user_from_classroom(user_id, course_id):
    remove_enrollment(
        get_contact_by_user_id(user_id), get_class_offering_by_id(course_id)
    )
    ClassroomMembership.objects.get(
        classroom=Classroom.objects.get(id=course_id), member_id=user_id
    ).delete()


def add_user_to_classroom(user_id, course_id, member_type):
    class_offering = get_class_offering_by_id(course_id)
    ClassroomMembership.objects.create(
        classroom=Classroom.objects.get(id=course_id),
        member=DjangoUser.objects.get(id=user_id),
        membership_type=member_type,
    )
    ClassEnrollment.objects.create(
        created_by=class_offering.created_by,
        contact=get_contact_by_user_id(user_id),
        status="Enrolled",
        class_offering=class_offering,
    )


def remove_enrollment(contact, class_offering):
    old_enrollment = ClassEnrollment.objects.get(
        contact=contact, status="Enrolled", class_offering=class_offering
    )
    created_by = old_enrollment.created_by
    old_enrollment.delete()
    return created_by


def get_contact_by_user_id(id):
    return Contact.objects.get(
        client_id=UserProfile.objects.get(user_id=id).salesforce_id
    )


def get_class_offering_by_id(id):
    course_name = get_course_name_by_id(id)
    return ClassOffering.objects.get(name=course_name)


def get_course_name_by_id(id):
    return Classroom.objects.get(id=id).course


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


def distribute_forms(request, posted_form, user_list):
    bulk_create_form_distributions(posted_form, user_list)
    messages.add_message(request, messages.SUCCESS, "Form Distributed Successfully")


def bulk_create_form_distributions(form, users):
    form_dists = [
        FormDistribution(form=form, user=user, submitted=False) for user in users
    ]
    FormDistribution.objects.bulk_create(form_dists)


def create_form_distribution(posted_form, user):
    dist = FormDistribution(form=posted_form, user=user, submitted=False)
    dist.save()


def get_outstanding_forms():
    outstanding_form_dict = {}
    for form in Form.objects.all():
        distributions = FormDistribution.objects.filter(form=form)
        outstanding_form_dict.update({form.name: distributions})
    return outstanding_form_dict


def email_form_notification(request, form, email_list):
    subject = form.cleaned_data.get("subject")
    msg_html = render_to_string(
        "email_templates/post_form_email.html",
        {
            "subject": subject,
            "message": form.cleaned_data.get("notification"),
            "from": DjangoUser.objects.get(id=request.user.id),
        },
    )
    text_content = "You are being notified about something"
    recipient_list = [
        "tyler.iams@gmail.com",
        "iams.sophia@gmail.com",
    ]  # Will replace with email_list
    email = EmailMultiAlternatives(
        subject, text_content, settings.EMAIL_HOST_USER, recipient_list
    )
    email.attach_alternative(msg_html, "text/html")
    email.attach_file(str(Form.objects.get(name=request.POST.get("notify_about")).form))
    email.send()
    messages.add_message(request, messages.SUCCESS, "Recipients Successfully Emailed")


def mark_announcement_dismissed(announcement, user):
    announcement = AnnouncementDistribution.objects.get(
        announcement_id=announcement.id, user_id=user.id
    )
    announcement.dismissed = True
    announcement.save()


def mark_notification_acknowledged(notification):
    notification.acknowledged = True
    notification.save()


def update_session(request, form):
    session = Session.objects.get(id=request.POST.get("session_id"))
    if request.POST.get("change_title"):
        session.title = form.cleaned_data.get("title")
        messages.add_message(request, messages.SUCCESS, "Session Title Updated")
    elif request.POST.get("change_description"):
        session.description = form.cleaned_data.get("description")
        messages.add_message(request, messages.SUCCESS, "Session Description Updated")
    elif request.POST.get("change_lesson_plan"):
        session.lesson_plan = form.cleaned_data.get("lesson_plan")
        messages.add_message(request, messages.SUCCESS, "Session Lesson Plan Updated")
    elif request.POST.get("change_activity"):
        session.activity = form.cleaned_data.get("activity")
        messages.add_message(request, messages.SUCCESS, "Session Activity Updated")
    elif request.POST.get("change_lecture"):
        session.lecture = form.cleaned_data.get("lecture")
        messages.add_message(request, messages.SUCCESS, "Session Lecture Updated")
    elif request.POST.get("change_video"):
        session.video = form.cleaned_data.get("video")
        messages.add_message(request, messages.SUCCESS, "Session Video Updated")
    else:
        messages.add_message(request, messages.WARNING, "Session Not Updated (Checkboxes?)")
    session.save()


def get_class_member_dict(classroom):
    teacher = get_users_of_type_from_classroom(classroom, "teacher").first()
    teacher_id = teacher.id
    teacher_assistant = get_users_of_type_from_classroom(
        classroom, "teacher_assistant"
    ).first()
    teacher_assistant_id = teacher_assistant.id
    return {
        "teacher": teacher,
        "teacher_id": teacher_id,
        "teacher_assistant": teacher_assistant,
        "teacher_assistant_id": teacher_assistant_id,
        "volunteers": get_users_of_type_from_classroom(classroom, "volunteer"),
        "students": get_users_of_type_from_classroom(classroom, "student"),
    }


def get_course_attendance_statistic(course_id):
    try:
        return Classroom.objects.get(id=course_id).attendance_summary.get(
            "attendance_statistic"
        )
    except AttributeError:
        return 0.0


def get_my_announcements(request, group):
    classroom = get_classroom_by_django_user(request.user)
    announcements = (
        Announcement.objects.filter(recipient_groups=Group.objects.get(name=group))
        | Announcement.objects.filter(recipient_classrooms=classroom)
    ).distinct()
    announcement_distributions = AnnouncementDistribution.objects.filter(
        announcement__in=announcements, user_id=request.user.id, dismissed=False
    )
    return announcement_distributions


def get_my_forms(request, group):
    classroom = get_classroom_by_django_user(request.user)
    forms = (
        Form.objects.filter(recipient_groups=Group.objects.get(name=group))
        | Form.objects.filter(recipient_classrooms=classroom)
    ).distinct()
    form_distributions = FormDistribution.objects.filter(
        form__in=forms, user_id=request.user.id, submitted=False
    )
    return form_distributions
