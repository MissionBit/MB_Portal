# Generated by Django 2.2.1 on 2019-06-25 04:27

from django.db import migrations
import salesforce.backend.operations
import salesforce.fields


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0021_auto_20190625_0415'),
    ]

    operations = [
        migrations.AlterField(
            model_name='classoffering',
            name='course_short_name',
            field=salesforce.fields.CharField(blank=True, db_column='Course_short_name__c', max_length=80, null=True, verbose_name='Course short name'),
        ),
        migrations.AlterField(
            model_name='classoffering',
            name='name',
            field=salesforce.fields.CharField(blank=True, default=salesforce.backend.operations.DefaultedOnCreate(), max_length=80, null=True, verbose_name='Class Offering Name'),
        ),
    ]
