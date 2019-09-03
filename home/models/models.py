from time import strftime
from secrets import token_urlsafe
from django.db import models as mdls
from django.contrib.auth.models import User as DjangoUser
from django.contrib.auth.models import Group
from django.contrib.postgres.fields import JSONField
from django.db.models.signals import post_save
from django.dispatch import receiver
from .salesforce import ClassOffering
from home.choices import *
from werkzeug import secure_filename
from django_q.models import Task


def get_name(self):
    return "%s %s" % (self.first_name, self.last_name)


DjangoUser.add_to_class("__str__", get_name)

Task.add_to_class("minutes", "minutes")


def upload_to(instance, filename):
    return "/".join(
        [
            secure_filename(type(instance).__name__),
            strftime("%Y/%m/%d"),
            instance.id or "0",
            token_urlsafe(8),
            secure_filename(filename),
        ]
    )


class UserProfile(mdls.Model):
    user = mdls.OneToOneField(DjangoUser, on_delete=mdls.CASCADE)
    change_pwd = mdls.BooleanField(default=False)
    date_of_birth = mdls.DateField(default="1901-01-01")
    salesforce_id = mdls.CharField(default="xxxxxx19010101", max_length=14)

    @receiver(post_save, sender=DjangoUser)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            UserProfile.objects.create(user=instance)

    @receiver(post_save, sender=DjangoUser)
    def save_user_profile(sender, instance, **kwargs):
        instance.userprofile.save()


class Classroom(mdls.Model):
    course = mdls.CharField(max_length=255, choices=COURSE_CHOICES)
    members = mdls.ManyToManyField(DjangoUser, through="ClassroomMembership")
    attendance_summary = JSONField(default=None, null=True)
    forum_title = mdls.CharField(max_length=240, default=None, null=True)
    forum = mdls.URLField(default=None, null=True)
    start_date = mdls.DateField(null=True)
    end_date = mdls.DateField(null=True)
    meeting_days = mdls.CharField(max_length=80, null=True)

    def __str__(self):
        return "%s" % (self.course)


class ClassroomMembership(mdls.Model):
    member = mdls.ForeignKey(
        DjangoUser, related_name="classroom_member", on_delete=mdls.CASCADE
    )
    classroom = mdls.ForeignKey(
        Classroom, related_name="membership_classroom", on_delete=mdls.CASCADE
    )
    membership_type = mdls.CharField(
        max_length=240, choices=CLASSROOM_MEMBERSHIP_CHOICES
    )


class Session(mdls.Model):
    title = mdls.CharField(max_length=240, default="No Title")
    description = mdls.TextField(max_length=2000, default="No Description Available")
    lesson_plan = mdls.FileField(default=None, upload_to=upload_to)
    lecture = mdls.FileField(default=None, upload_to=upload_to)
    video = mdls.URLField(default=None, null=True)
    activity = mdls.FileField(default=None, upload_to=upload_to)
    classroom = mdls.ForeignKey(
        Classroom,
        related_name="classroom_session",
        on_delete=mdls.CASCADE,
        default=None,
    )
    date = mdls.DateField(default="1901-01-01")

    def __str__(self):
        return "%s - %s" % (self.classroom, self.date)


class Resource(mdls.Model):
    title = mdls.TextField(max_length=240, default="No Title")
    description = mdls.TextField(max_length=2000)
    link = mdls.URLField(default=None, null=True)
    file = mdls.FileField(default=None, null=True, upload_to=upload_to)
    classroom = mdls.ForeignKey(
        Classroom, related_name="classroom_resource", on_delete=mdls.CASCADE
    )
    session = mdls.ForeignKey(
        Session, related_name="session_resource", on_delete=mdls.CASCADE
    )

    def __str__(self):
        return "%s - %s" % (self.title, self.session)


class Attendance(mdls.Model):
    date = mdls.DateField(default="1901-01-01")
    student = mdls.ForeignKey(
        DjangoUser, related_name="student", on_delete=mdls.CASCADE
    )
    presence = mdls.CharField(max_length=100, default="Unassigned")
    session = mdls.ForeignKey(
        Session, related_name="session", on_delete=mdls.CASCADE, default=None
    )
    classroom = mdls.ForeignKey(
        Classroom,
        related_name="attendance_classroom",
        on_delete=mdls.CASCADE,
        default=None,
    )
    notes = mdls.TextField(max_length=500, default="")


class Announcement(mdls.Model):
    title = mdls.CharField(max_length=240, unique=True)
    announcement = mdls.TextField(max_length=2500)
    posted = mdls.DateTimeField(db_index=True, auto_now=True)
    recipient_groups = mdls.ManyToManyField(Group, related_name="user_groups")
    recipient_classrooms = mdls.ManyToManyField(
        Classroom, related_name="recipient_classroom"
    )
    email_recipients = mdls.BooleanField(null=False, default=False)
    created_by = mdls.ForeignKey(
        DjangoUser, related_name="user", on_delete=mdls.CASCADE
    )

    def __str__(self):
        return "%s, %s" % (self.title, self.posted)


class AnnouncementDistribution(mdls.Model):
    announcement = mdls.ForeignKey(
        Announcement, related_name="announcement_distributed", on_delete=mdls.CASCADE
    )
    user = mdls.ForeignKey(
        DjangoUser, related_name="announcement_user", on_delete=mdls.CASCADE
    )
    dismissed = mdls.BooleanField(null=False, default=False)

    def __str__(self):
        return "%s - %s - dismissed: %s" % (
            self.announcement,
            self.user,
            self.dismissed,
        )


class Esign(mdls.Model):
    name = mdls.CharField(max_length=240, unique=True)
    template = mdls.URLField()
    created_by = mdls.ForeignKey(
        DjangoUser,
        related_name="esign_creator_user",
        on_delete=mdls.CASCADE,
        default=False,
    )

    def __str__(self):
        return self.name


class Form(mdls.Model):
    name = mdls.CharField(max_length=240, unique=True)
    description = mdls.TextField(max_length=2500)
    form = mdls.FileField(upload_to=upload_to)
    esign = mdls.ForeignKey(
        Esign, related_name="esign_form", on_delete=mdls.CASCADE, null=True
    )
    posted = mdls.DateTimeField(db_index=True, auto_now=True)
    recipient_groups = mdls.ManyToManyField(Group, related_name="form_user_groups")
    recipient_classrooms = mdls.ManyToManyField(
        Classroom, related_name="form_recipient_classroom"
    )
    created_by = mdls.ForeignKey(
        DjangoUser, related_name="form_user", on_delete=mdls.CASCADE
    )

    def __str__(self):
        return self.name


class FormDistribution(mdls.Model):
    user = mdls.ForeignKey(
        DjangoUser, related_name="form_signer", on_delete=mdls.CASCADE
    )
    form = mdls.ForeignKey(
        Form, related_name="form_to_be_signed", on_delete=mdls.CASCADE
    )
    submitted = mdls.BooleanField(null=False, default=False)

    def __str__(self):
        return "%s, %s" % (self.user, self.form)


class Notification(mdls.Model):
    user = mdls.ForeignKey(
        DjangoUser, related_name="notified_user", on_delete=mdls.CASCADE
    )
    subject = mdls.CharField(max_length=240)
    notification = mdls.TextField(max_length=2500)
    email_recipients = mdls.BooleanField(null=False, default=False)
    form = mdls.ForeignKey(
        Form, related_name="notified_about_form", on_delete=mdls.CASCADE, null=True
    )
    attendance = mdls.ForeignKey(
        Attendance,
        related_name="notified_about_attendance",
        on_delete=mdls.CASCADE,
        null=True,
    )
    notified = mdls.DateTimeField(db_index=True, auto_now=True)
    created_by = mdls.ForeignKey(
        DjangoUser, related_name="notification_user", on_delete=mdls.CASCADE
    )
    acknowledged = mdls.BooleanField(null=False, default=False)

    def __str__(self):
        return "%s %s" % (self.subject, self.created_by)
