# Create your tasks here
from __future__ import absolute_import, unicode_literals
from celery import shared_task
from home.models.models import DjangoUser, UserProfile, Group
from home.models.salesforce import Contact
from staff.staff_views_helper import create_django_user_from_contact


@shared_task
def add_salesforce_contacts_to_postgres():
    """This method will identify contacts (students, teachers, and volunteers only)
    who exist in the salesforce database but do not exist in the postgres database, and
    add them to the local postgres database."""
    contacts = Contact.objects.filter(title__in=["Student", "Teacher", "Volunteer"])
    for contact in contacts:
        if not DjangoUser.objects.filter(first_name=contact.first_name,
                                         last_name=contact.last_name,
                                         email=contact.email).exists():
            create_django_user_from_contact(contact)


@shared_task
def sync_userprofile_data_with_salesforce_data():
    """This method will assure that contacts corresponding to existing django_users' userprofiles
    will have matching salesforce_id/client_id fields in the postgres and salesforce databases, respectively"""
    for user in UserProfile.objects.select_related('user').all():
        django_user = user.user
        try:
            contact = Contact.objects.get(first_name=django_user.first_name, last_name=django_user.last_name, email=django_user.email)
        except Contact.DoesNotExist:
            print("%s %s, id: %s - not found in salesfoce." % (django_user.first_name, django_user.last_name, django_user.id))
            continue
        if user.salesforce_id is not contact.client_id:
            user.date_of_birth = contact.birthdate
            user.salesforce_id = str(contact.client_id).lower()
            user.save()

