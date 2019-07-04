from django.test import TestCase, RequestFactory
from staff.views import *
from django.contrib.auth.models import User as DjangoUser
from django.urls import reverse
from rest_framework import status
from missionbit.settings import *

class BaseTestCase(TestCase):
    def create_authenticated_staff_user(self):
        user = DjangoUser.objects.create_user(
            username="testuser",
            email="test@email.com",
            first_name="testfirst",
            last_name="testlast",
            password="beautifulbutterfly125",
        )
        Group.objects.get_or_create(name="staff")
        staff_group = Group.objects.get(name="staff")
        staff_group.user_set.add(user)
        return user

    def create_authenticated_nonstaff_user(self):
        user = DjangoUser.objects.create_user(
            username="otherstafftestuser",
            email="othertest@email.com",
            first_name="othertestfirst",
            last_name="othertestlast",
            password="beautifulbutterfly125",
        )
        Group.objects.get_or_create(name="student")
        student_group = Group.objects.get(name="student")
        student_group.user_set.add(user)
        return user


class StaffViewsTest(BaseTestCase):
    databases = '__all__'

    def test_staff(self):
        self.client.force_login(self.create_authenticated_staff_user())
        response = self.client.get(reverse("staff"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTemplateUsed(response, "staff.html")
        self.client.force_login(self.create_authenticated_nonstaff_user())
        self.assertRaises(PermissionError)

    def test_user_management(self):
        self.client.force_login(self.create_authenticated_staff_user())
        response = self.client.get(reverse("user_management"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTemplateUsed(response, "user_management.html")
        self.client.force_login(self.create_authenticated_nonstaff_user())
        self.assertRaises(PermissionError)

    def test_create_staff_user(self):
        self.client.force_login(self.create_authenticated_staff_user())
        response = self.client.get(reverse("create_staff_user"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTemplateUsed(response, "create_staff_user.html")
        self.client.force_login(self.create_authenticated_nonstaff_user())
        self.assertRaises(PermissionError)

    def test_create_teacher_user(self):
        self.client.force_login(self.create_authenticated_staff_user())
        response = self.client.get(reverse("create_teacher_user"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTemplateUsed(response, "create_teacher_user.html")
        self.client.force_login(self.create_authenticated_nonstaff_user())
        self.assertRaises(PermissionError)

    def test_create_student_user(self):
        self.client.force_login(self.create_authenticated_staff_user())
        response = self.client.get(reverse("create_student_user"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTemplateUsed(response, "create_student_user.html")
        self.client.force_login(self.create_authenticated_nonstaff_user())
        self.assertRaises(PermissionError)

    def test_create_volunteer_user(self):
        self.client.force_login(self.create_authenticated_staff_user())
        response = self.client.get(reverse("create_volunteer_user"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTemplateUsed(response, "create_volunteer_user.html")
        self.client.force_login(self.create_authenticated_nonstaff_user())
        self.assertRaises(PermissionError)

    def test_my_account_staff(self):
        self.client.force_login(self.create_authenticated_staff_user())
        response = self.client.get(reverse("my_account_staff"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTemplateUsed(response, "my_account_staff.html")
        self.client.force_login(self.create_authenticated_nonstaff_user())
        self.assertRaises(PermissionError)

