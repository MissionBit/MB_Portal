# Generated by Django 2.2.3 on 2019-07-11 14:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0033_auto_20190711_1342'),
    ]

    operations = [
        migrations.AlterField(
            model_name='session',
            name='video',
            field=models.URLField(default=None, null=True),
        ),
    ]