# Create your tasks here
from __future__ import absolute_import, unicode_literals

from celery import shared_task


@shared_task
def hello():
    print("It's a beautiful day in the neighborhood")
