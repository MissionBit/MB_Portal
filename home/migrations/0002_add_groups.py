from django.db import models, migrations
from home.models.models import Group
from django.conf import settings


def add_groups(apps, schema_editor):
    Group.objects.get_or_create(name="Staff"),
    Group.objects.get_or_create(name="Student"),
    Group.objects.get_or_create(name="Teacher"),
    Group.objects.get_or_create(name="Volunteer"),
    Group.objects.get_or_create(name="Donor"),


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("auth", "0011_update_proxy_permissions"),
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(add_groups),
    ]
