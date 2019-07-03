from django.test import TestCase, RequestFactory
from student.views import *
from django.contrib.auth.models import User, Group
from django.urls import reverse
from rest_framework import status

"""
class BaseTestCase(TestCase):
    def create_authenticated_student_user(self):
        user = User.objects.create_user(
            username="testuser",
            email="test@email.com",
            first_name="testfirst",
            last_name="testlast",
            password="beautifulbutterfly125",
        )
        Group.objects.get_or_create(name="student")
        student_group = Group.objects.get(name="student")
        student_group.user_set.add(user)
        return user

    def create_authenticated_nonstudent_user(self):
        user = User.objects.create_user(
            username="otherstafftestuser",
            email="othertest@email.com",
            first_name="othertestfirst",
            last_name="othertestlast",
            password="beautifulbutterfly125",
        )
        Group.objects.get_or_create(name="staff")
        staff_group = Group.objects.get(name="staff")
        staff_group.user_set.add(user)
        return user


class StudentViewsTest(BaseTestCase):
    def test_student(self):
        request = RequestFactory().get(reverse("home-home"))
        request.user = self.create_authenticated_nonstudent_user()
        response = student(request)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        request.user = self.create_authenticated_student_user()
        response = student(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
"""
