# Generated by Django 2.2.1 on 2019-06-25 04:37

from django.db import migrations
import salesforce.fields


class Migration(migrations.Migration):

    dependencies = [("home", "0023_auto_20190625_0436")]

    operations = [
        migrations.AlterField(
            model_name="classoffering",
            name="course_short_name",
            field=salesforce.fields.CharField(
                blank=True,
                db_column="Course_short_name__c",
                default="shortname",
                max_length=1300,
                null=True,
                verbose_name="Course short name",
            ),
        )
    ]
