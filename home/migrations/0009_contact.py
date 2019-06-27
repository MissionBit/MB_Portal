# Generated by Django 2.2.1 on 2019-06-20 23:14

from django.db import migrations
import django.db.models.deletion
import salesforce.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [("home", "0008_delete_users")]

    operations = [
        migrations.CreateModel(
            name="Contact",
            fields=[
                (
                    "id",
                    salesforce.fields.SalesforceAutoField(
                        auto_created=True,
                        db_column="Id",
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "is_deleted",
                    salesforce.fields.BooleanField(
                        default=False, verbose_name="Deleted"
                    ),
                ),
                ("last_name", salesforce.fields.CharField(max_length=80)),
                (
                    "first_name",
                    salesforce.fields.CharField(blank=True, max_length=40, null=True),
                ),
                (
                    "salutation",
                    salesforce.fields.CharField(
                        blank=True,
                        choices=[
                            ("Mr.", "Mr."),
                            ("Ms.", "Ms."),
                            ("Mrs.", "Mrs."),
                            ("Dr.", "Dr."),
                            ("Prof.", "Prof."),
                        ],
                        max_length=40,
                        null=True,
                    ),
                ),
                (
                    "middle_name",
                    salesforce.fields.CharField(blank=True, max_length=40, null=True),
                ),
                (
                    "suffix",
                    salesforce.fields.CharField(blank=True, max_length=40, null=True),
                ),
                (
                    "name",
                    salesforce.fields.CharField(
                        max_length=121, verbose_name="Full Name"
                    ),
                ),
                (
                    "master_record",
                    salesforce.fields.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        related_name="contact_masterrecord_set",
                        to="home.Contact",
                    ),
                ),
            ],
            options={
                "verbose_name": "Contact",
                "verbose_name_plural": "Contacts",
                "db_table": "Contact",
                "abstract": False,
                "base_manager_name": "objects",
            },
        )
    ]