from django.db import models as mdls
from django.contrib.auth.models import User as DjangoUser
from django.db.models.signals import post_save
from django.dispatch import receiver
from home.choices import *


class UserProfile(mdls.Model):
    user = mdls.OneToOneField(DjangoUser, on_delete=mdls.CASCADE)
    change_pwd = mdls.BooleanField(default=False)
    date_of_birth = mdls.DateField(default="1901-01-01")
    salesforce_id = mdls.CharField(default="xxxxxx01011901", max_length=14)

    @receiver(post_save, sender=DjangoUser)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            UserProfile.objects.create(user=instance)

    @receiver(post_save, sender=DjangoUser)
    def save_user_profile(sender, instance, **kwargs):
        instance.userprofile.save()


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
