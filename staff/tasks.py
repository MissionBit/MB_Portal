# Create your tasks here
from __future__ import absolute_import, unicode_literals
from celery import shared_task

from home.models.models import (
    DjangoUser,
    UserProfile,
    Classroom,
    Notification,
    Session,
    Attendance,
)
from home.models.salesforce import Contact, ClassOffering, ClassMeeting, ClassAttendance
from staff.staff_views_helper import (
    create_django_user_from_contact,
    generate_classroom_sessions_and_attendance,
    get_django_user_from_contact
)
from datetime import datetime


@shared_task
def add_salesforce_contacts_to_postgres():
    """This method will identify contacts (students, teachers, and volunteers only)
    who exist in the salesforce database but do not exist in the postgres database, and
    add them to the local postgres database."""
    contacts = Contact.objects.filter(title__in=["Student", "Teacher", "Volunteer"])
    for contact in contacts:
        if not DjangoUser.objects.filter(
            first_name=contact.first_name,
            last_name=contact.last_name,
            email=contact.email,
        ).exists():
            create_django_user_from_contact(contact)


@shared_task
def sync_userprofile_data_with_salesforce_data():
    """This method will assure that contacts corresponding to existing django_users' userprofiles
    will have matching salesforce_id/client_id fields in the postgres and salesforce databases, respectively"""
    for user in UserProfile.objects.select_related("user").all():
        django_user = user.user
        try:
            contact = Contact.objects.get(
                first_name=django_user.first_name,
                last_name=django_user.last_name,
                email=django_user.email,
            )
        except Contact.DoesNotExist:
            continue
        if user.salesforce_id != contact.client_id:
            user.date_of_birth = contact.birthdate
            user.salesforce_id = str(contact.client_id).lower()
            user.save()


@shared_task
def cross_reference_classrooms_with_class_offerings():
    """This method will periodically check for differences in classroom start_date, end_date and
    meeting_days with class_offering parameters of the same names.  If a difference is detected,
    a notification for Staff users will be created, which will prompt them to sync the data, and
    warn them that doing so will destroy and recreate data."""
    classrooms = Classroom.objects.all()
    for class_offering in ClassOffering.objects.filter(
        academic_semester="Fall 2019", mbportal_id__isnull=False
    ):
        try:
            classroom = classrooms.get(id=class_offering.mbportal_id)
            if (
                str(class_offering.start_date) != str(classroom.start_date)
                or str(class_offering.end_date) != str(classroom.end_date)
                or str(class_offering.meeting_days) != str(class_offering.meeting_days)
            ):
                notifications = [
                    Notification(
                        subject="Classroom Meeting Dates Changed in Salesforce",
                        notification="The start date, end date or meeting days for %s has been changed in the Salesforce database.  "
                        "This may affect the accuracy of current Class Meetings, Curriculum and Attendance data.  "
                        "If you do not want Class Meeting, Curriculum, and Attendance Data overwritten, "
                        "please reach out to Mission Bit's developer team for assistance.  "
                        "To overwrite the current data with correct Sessions, Class Meetings and Curriculum, "
                        "please click 'Reset Course Data' on the course's page."
                        % class_offering.name,
                        email_recipients=False,
                        acknowledged=False,
                        created_by=user,
                        user=user,
                    )
                    for user in DjangoUser.objects.filter(groups__name="staff")
                ]
                Notification.objects.bulk_create(notifications)
        except Classroom.DoesNotExist:
            pass


@shared_task
def reset_classroom_data(classroom_id):
    """This method takes a classroom id as a parameter, and resets all of the sessions and attendance
    data in the postgres and salesforce databases"""
    classroom = Classroom.objects.get(id=classroom_id)
    classroom.attendance_summary = {"attendance_statistic": 0.0}
    class_offering = ClassOffering.objects.get(mbportal_id=classroom.id)
    classroom.course = class_offering.name
    classroom.start_date = class_offering.start_date
    classroom.end_date = class_offering.end_date
    classroom.meeting_days = class_offering.meeting_days
    classroom.save()
    Session.objects.filter(classroom=classroom).delete()
    Attendance.objects.filter(classroom=classroom).delete()
    ClassMeeting.objects.filter(class_offering=class_offering).delete()
    generate_classroom_sessions_and_attendance(classroom)


@shared_task
def sync_attendance_with_salesforce_attendance():
    """This method syncs attendance data with the data in salesforce"""
    for classroom in Classroom.objects.all():
        attendances = Attendance.objects.filter(
            date__range=[classroom.start_date, datetime.today().date()],
            classroom=classroom,
        )
        class_meetings = ClassMeeting.objects.filter(
            class_offering__mbportal_id=classroom.id,
            date__range=[classroom.start_date, datetime.today().date()],
        )
        class_attendances = ClassAttendance.objects.filter(
            class_meeting__in=[meeting for meeting in class_meetings]
        )
        for class_attendance in class_attendances:
            attendance = attendances.get(
                date=class_attendance.class_meeting_date,
                student=get_django_user_from_contact(class_attendance.contact),
            )
            if attendance.presence != "Unassigned":
                class_attendance.status = attendance.presence
                class_attendance.save()
