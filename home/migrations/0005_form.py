from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("auth", "0011_update_proxy_permissions"),
        ("home", "0003_classroom_attendance_summary"),
    ]

    operations = [
        migrations.CreateModel(
            name="Form",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=240, unique=True)),
                ("form", models.FileField(upload_to="documents/")),
                ("posted", models.DateTimeField(auto_now=True, db_index=True)),
                (
                    "created_by",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="form_user",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "recipient_classrooms",
                    models.ManyToManyField(
                        related_name="form_recipient_classroom", to="home.Classroom"
                    ),
                ),
                (
                    "recipient_groups",
                    models.ManyToManyField(
                        related_name="form_user_groups", to="auth.Group"
                    ),
                ),
            ],
        )
    ]
