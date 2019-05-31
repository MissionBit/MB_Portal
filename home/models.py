from django.db import models

# Create your models here.

class Users(models.Model):
    STAFF = 'staff'
    TEACHER = 'teacher'
    STUDENT = 'student'
    VOLUNTEER = 'volunteer'
    ROLE_CHOICES = [
        (STAFF, 'Staff'),
        (TEACHER, 'Teacher'),
        (STUDENT, 'Student'),
        (VOLUNTEER, 'Volunteer')
    ]
    username = models.CharField(max_length=100, default='none')
    email = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    role = models.CharField(max_length=100, choices=ROLE_CHOICES, default=STUDENT)