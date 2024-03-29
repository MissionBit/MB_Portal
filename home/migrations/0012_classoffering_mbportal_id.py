# Generated by Django 2.2.4 on 2019-09-02 20:52

from django.db import migrations
import salesforce.fields


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0011_auto_20190902_0127'),
    ]

    operations = [
        migrations.AddField(
            model_name='classoffering',
            name='mbportal_id',
            field=salesforce.fields.DecimalField(blank=True, db_column='MBPortal_id__c', decimal_places=0, help_text='This will be automatically set by the Mission Bit Portal, and should not be altered.', max_digits=8, null=True, unique=True, verbose_name='MBPortal_id'),
        ),
    ]
