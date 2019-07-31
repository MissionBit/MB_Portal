from django.db import models as mdls
from django.contrib.auth.models import User as DjangoUser
from django.contrib.auth.models import Group
from django.contrib.postgres.fields import JSONField
from django.db.models.signals import post_save
from django.dispatch import receiver
from home.choices import *


def get_name(self):
    return "%s %s" % (self.first_name, self.last_name)


DjangoUser.add_to_class("__str__", get_name)


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


class Session(mdls.Model):
    description = mdls.TextField(max_length=2000, default="No Description Available")
    lesson_plan = mdls.FileField(default=None)
    lecture = mdls.FileField(default=None)
    video = mdls.URLField(default=None, null=True)
    activity = mdls.FileField(default=None)


class Classroom(mdls.Model):
    course = mdls.CharField(max_length=255, choices=COURSE_CHOICES)
    teacher = mdls.ForeignKey(
        DjangoUser, related_name="classroom_lead_teacher", on_delete=mdls.CASCADE
    )
    teacher_assistant = mdls.ForeignKey(
        DjangoUser, related_name="classroom_teacher_assistant", on_delete=mdls.CASCADE
    )
    volunteers = mdls.ManyToManyField(DjangoUser, related_name="classroom_volunteers")
    students = mdls.ManyToManyField(DjangoUser, related_name="classroom_students")
    attendance_summary = JSONField(default=None, null=True)

    def __str__(self):
        return "%s - %s, %s" % (
            self.course,
            self.teacher.last_name,
            self.teacher.first_name,
        )


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
    announcement = mdls.ForeignKey(Announcement, related_name="announcement_distributed", on_delete=mdls.CASCADE)
    user = mdls.ForeignKey(DjangoUser, related_name="announcement_user", on_delete=mdls.CASCADE)
    dismissed = mdls.BooleanField(null=False, default=False)

    def __str__(self):
        return "%s - %s - dismissed: %s" % (self.announcement, self.user, self.dismissed)


class Esign(mdls.Model):
    name = mdls.CharField(max_length=240, unique=True)
    template = mdls.URLField()
    created_by = mdls.ForeignKey(
        DjangoUser, related_name="esign_creator_user", on_delete=mdls.CASCADE, default=False
    )

    def __str__(self):
        return self.name


class Form(mdls.Model):
    name = mdls.CharField(max_length=240, unique=True)
    description = mdls.TextField(max_length=2500)
    form = mdls.FileField(upload_to="documents/")
    esign = mdls.ForeignKey(Esign, related_name="esign_form", on_delete=mdls.CASCADE, null=True)
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
    user = mdls.ForeignKey(DjangoUser, related_name="form_signer", on_delete=mdls.CASCADE)
    form = mdls.ForeignKey(Form, related_name="form_to_be_signed", on_delete=mdls.CASCADE)
    submitted = mdls.BooleanField(null=False, default=False)

    def __str__(self):
        return "%s, %s" % (self.user, self.form)


class Notification(mdls.Model):
    user = mdls.ForeignKey(DjangoUser, related_name="notified_user", on_delete=mdls.CASCADE)
    subject = mdls.CharField(max_length=240)
    notification = mdls.TextField(max_length=2500)
    email_recipients = mdls.BooleanField(null=False, default=False)
    form = mdls.ForeignKey(Form, related_name="notified_about_form", on_delete=mdls.CASCADE, null=True)
    attendance = mdls.ForeignKey(Attendance, related_name="notified_about_attendance", on_delete=mdls.CASCADE, null=True)
    notified = mdls.DateTimeField(db_index=True, auto_now=True)
    created_by = mdls.ForeignKey(
        DjangoUser, related_name="notification_user", on_delete=mdls.CASCADE
    )
    acknowledged = mdls.BooleanField(null=False, default=False)

    def __str__(self):
        return "%s %s" % (self.subject, self.created_by)
