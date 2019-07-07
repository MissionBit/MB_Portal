from django.test import TestCase, RequestFactory
from staff.views import *
from django.contrib.auth.models import User as DjangoUser
from home.models.models import Classroom
from django.urls import reverse
from rest_framework import status
from home.models.salesforce import (
    Contact,
    User,
    Account,
    ClassOffering,
    ClassEnrollment,
)


class BaseTestCase(TestCase):
    def setUp(self) -> None:
        Group.objects.create(name="student")
        Group.objects.create(name="teacher")
        Group.objects.create(name="volunteer")
        Group.objects.create(name="donor")
        Group.objects.create(name="staff")
        teacher = DjangoUser.objects.create_user(
            username="classroom_teacher",
            email="teacher@email.com",
            first_name="testfirst",
            last_name="testlast",
            password="testpassword",
        )
        Group.objects.get(name='teacher').user_set.add(teacher)
        t_a = DjangoUser.objects.create_user(
            username="classroom_teacher2",
            email="teacher2@email.com",
            first_name="test2first",
            last_name="test2last",
            password="testpassword",
        )
        Group.objects.get(name='teacher').user_set.add(t_a)
        student = DjangoUser.objects.create_user(
            username="classroom_student",
            email="student@email.com",
            first_name="studentfirst",
            last_name="studentlast",
            password="testpassword",
        )
        Group.objects.get(name='teacher').user_set.add(student)
        volunteer = DjangoUser.objects.create_user(
            username="classroom_vol",
            email="teacher2@email.com",
            first_name="volfirst",
            last_name="vollast",
            password="testpassword",
        )
        Group.objects.get(name='teacher').user_set.add(volunteer)
        classroom = Classroom.objects.create(
            course="Test_Course",
            teacher=teacher,
            teacher_assistant=t_a
        )
        classroom.students.add(student)
        classroom.volunteers.add(volunteer)

    def create_staff_user(self):
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

    def create_nonstaff_user(self):
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

    def valid_create_user_form(self, group):
        return {
            "first_name": "test_user",
            "last_name": "test_user",
            "email": "test@email.com",
            "birthdate": "01/01/2001",
            "owner": User.objects.filter(is_active=True).first().id,
            "title": group,
        }

    def valid_create_classroom_form(self):
        return {
            "course": ClassOffering
        }


class StaffViewsTest(BaseTestCase):
    databases = '__all__'

    def test_staff(self):
        self.client.force_login(self.create_staff_user())
        response = self.client.get(reverse("staff"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTemplateUsed(response, "staff.html")
        self.client.force_login(self.create_nonstaff_user())
        self.assertRaises(PermissionError)

    def test_user_management(self):
        self.client.force_login(self.create_staff_user())
        response = self.client.get(reverse("user_management"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTemplateUsed(response, "user_management.html")
        self.client.force_login(self.create_nonstaff_user())
        self.assertRaises(PermissionError)

    def test_create_staff_user(self):
        self.client.force_login(self.create_staff_user())
        response = self.client.get(reverse("create_staff_user"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTemplateUsed(response, "create_staff_user.html")
        response = self.client.post(reverse("create_staff_user"), self.valid_create_user_form("staff"))
        Contact.objects.get(client_id="testes20010101").delete()
        self.assertEqual(response.url, reverse("staff"))
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.client.force_login(self.create_nonstaff_user())
        self.assertRaises(PermissionError)

    def test_create_staff_user_invalid_form(self):
        self.client.force_login(self.create_staff_user())
        response = self.client.post(reverse("create_staff_user"), {})
        self.assertEqual(response.url, reverse("staff"))
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)

    def test_create_teacher_user(self):
        self.client.force_login(self.create_staff_user())
        response = self.client.get(reverse("create_teacher_user"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTemplateUsed(response, "create_teacher_user.html")
        response = self.client.post(reverse("create_teacher_user"), self.valid_create_user_form("teacher"))
        Contact.objects.get(client_id="testes20010101").delete()
        self.assertEqual(response.url, reverse("staff"))
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.client.force_login(self.create_nonstaff_user())
        self.assertRaises(PermissionError)

    def test_create_teacher_user_invalid_form(self):
        self.client.force_login(self.create_staff_user())
        response = self.client.post(reverse("create_teacher_user"), {})
        self.assertEqual(response.url, reverse("staff"))
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)

    def test_create_student_user(self):
        self.client.force_login(self.create_staff_user())
        response = self.client.get(reverse("create_student_user"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTemplateUsed(response, "create_student_user.html")
        response = self.client.post(reverse("create_student_user"), self.valid_create_user_form("student"))
        Contact.objects.get(client_id="testes20010101").delete()
        self.assertEqual(response.url, reverse("staff"))
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.client.force_login(self.create_nonstaff_user())
        self.assertRaises(PermissionError)

    def test_create_student_user_invalid_form(self):
        self.client.force_login(self.create_staff_user())
        response = self.client.post(reverse("create_student_user"), {})
        self.assertEqual(response.url, reverse("staff"))
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)

    def test_create_volunteer_user(self):
        self.client.force_login(self.create_staff_user())
        response = self.client.get(reverse("create_volunteer_user"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTemplateUsed(response, "create_volunteer_user.html")
        response = self.client.post(reverse("create_volunteer_user"), self.valid_create_user_form("volunteer"))
        Contact.objects.get(client_id="testes20010101").delete()
        self.assertEqual(response.url, reverse("staff"))
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.client.force_login(self.create_nonstaff_user())
        self.assertRaises(PermissionError)

    def test_create_volunteer_user_invalid_form(self):
        self.client.force_login(self.create_staff_user())
        response = self.client.post(reverse("create_volunteer_user"), {})
        self.assertEqual(response.url, reverse("staff"))
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)

    def test_my_account_staff(self):
        self.client.force_login(self.create_staff_user())
        response = self.client.get(reverse("my_account_staff"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTemplateUsed(response, "my_account_staff.html")
        self.client.force_login(self.create_nonstaff_user())
        self.assertRaises(PermissionError)

    def test_classroom_management(self):
        self.client.force_login(self.create_staff_user())
        response = self.client.get(reverse("classroom_management"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTemplateUsed(response, "classroom_management.html")

    def test_create_classroom(self):
        self.client.force_login(self.create_staff_user())
        response = self.client.get(reverse("create_classroom"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTemplateUsed(response, "create_classroom.html")
        response = self.client.post(reverse("create_classroom"), )
