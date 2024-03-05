from django.test import TestCase, RequestFactory
from staff.views import *
from django.contrib.auth.models import User as DjangoUser
from home.models.models import Classroom, UserProfile, ClassroomMembership
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
        teacher = DjangoUser.objects.create_user(
            username="classroom_teacher",
            email="teacher@email.com",
            first_name="class",
            last_name="teacher",
            password="testpassword",
        )
        teacher.userprofile.salesforce_id = "clatea19010101"
        teacher.save()
        Group.objects.get(name="teacher").user_set.add(teacher)
        t_a = DjangoUser.objects.create_user(
            username="classroom_teacher2",
            email="teacher2@email.com",
            first_name="tassist",
            last_name="user",
            password="testpassword",
        )
        t_a.userprofile.salesforce_id = "tasuse19010101"
        t_a.save()
        Group.objects.get(name="teacher").user_set.add(t_a)
        student = DjangoUser.objects.create_user(
            username="classroom_student",
            email="student@email.com",
            first_name="student",
            last_name="user",
            password="testpassword",
        )
        student.userprofile.salesforce_id = "stuuse19010101"
        student.save()
        Group.objects.get(name="teacher").user_set.add(student)
        volunteer = DjangoUser.objects.create_user(
            username="classroom_vol",
            email="teacher2@email.com",
            first_name="volunteer",
            last_name="user",
            password="testpassword",
        )
        volunteer.userprofile.salesforce_id = "voluse19010101"
        volunteer.save()
        Group.objects.get(name="teacher").user_set.add(volunteer)
        classroom = Classroom.objects.create(course="Test_Course")
        ClassroomMembership.objects.create(
            member=teacher, classroom=classroom, membership_type="teacher"
        )
        ClassroomMembership.objects.create(
            member=t_a, classroom=classroom, membership_type="teacher_assistant"
        )
        ClassroomMembership.objects.create(
            member=volunteer, classroom=classroom, membership_type="volunteer"
        )
        ClassroomMembership.objects.create(
            member=student, classroom=classroom, membership_type="student"
        )

    def create_staff_user(self):
        user = DjangoUser.objects.create_user(
            username="testuser",
            email="test@email.com",
            first_name="testfirst",
            last_name="testlast",
            password="top_secret125",
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
            password="top_secret125",
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
            "birthdate": "01/01/1901",
            "owner": User.objects.filter(is_active=True).first().id,
            "title": group,
        }

    def valid_create_class_offering_form(self):
        return {
            "name": "Test Course",
            "course": "Android Game Design",
            "location": Account.objects.get_or_create(name="Test_Org", npe01_systemis_individual=False)[0].id,
            "created_by": User.objects.filter(is_active=True).first().id,
            "start_date": "2019-07-07",
            "end_date": "2019-09-09",
            "description": "This is a test classroom",
            "instructor": self.get_or_create_test_teacher().id,
            "meeting_days": "M/W",
        }

    def valid_create_classroom_form(self):
        return {
            "course": self.get_or_create_test_course().id,
            "teacher": self.get_or_create_test_teacher().id,
            "teacher_assistant": self.get_or_create_test_teacher().id,
            "volunteers": self.get_or_create_test_volunteer().id,
            "students": self.get_or_create_test_student().id,
            "created_by": User.objects.filter(is_active=True).first().id,
        }

    def get_or_create_test_course(self):
        course = ClassOffering.objects.get_or_create(
            name="Test Course",
            course="Android Game Design",
            location=Account.objects.get_or_create(name="Test_Org", npe01_systemis_individual=False)[0],
            created_by=User.objects.filter(is_active=True).first(),
            start_date="2019-07-07",
            end_date="2019-09-09",
            instructor=self.get_or_create_test_teacher(),
            meeting_days="M/W",
        )
        return course[0]

    def get_or_create_test_teacher(self):
        contact = Contact.objects.get_or_create(
            first_name="classroom",
            last_name="teacher",
            email="clatea@gmail.com",
            birthdate="1901-01-01",
            title="Teacher",
            owner=User.objects.filter(is_active=True).first(),
            race="White",
            which_best_describes_your_ethnicity="Hispanic/Latinx",
            gender="Female",
        )
        return contact[0]

    def get_or_create_test_student(self):
        contact = Contact.objects.get_or_create(
            first_name="student",
            last_name="user",
            email="clastu@gmail.com",
            birthdate="1901-01-01",
            title="Student",
            owner=User.objects.filter(is_active=True).first(),
            race="White",
            which_best_describes_your_ethnicity="Hispanic/Latinx",
            gender="Female",
        )
        return contact[0]

    def get_or_create_test_volunteer(self):
        contact = Contact.objects.get_or_create(
            first_name="volunteer",
            last_name="user",
            email="clavol@gmail.com",
            birthdate="1901-01-01",
            title="Volunteer",
            owner=User.objects.filter(is_active=True).first(),
            race="White",
            which_best_describes_your_ethnicity="Hispanic/Latinx",
            gender="Female",
        )
        return contact[0]

    def valid_make_announcement_form(self):
        return {
            "title": "Test Announcement",
            "announcement": "This is the test announcement",
            "email_recipients": True,
        }


class StaffViewsTest(BaseTestCase):
    databases = "__all__"

    def test_staff(self):
        self.client.force_login(self.create_staff_user())
        response = self.client.get(reverse("staff"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTemplateUsed(response, "staff.html")
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
        response = self.client.post(
            reverse("create_classroom"), self.valid_create_classroom_form()
        )
        ClassOffering.objects.get(name="Summer 2019 - Android - Test_Org - M/W - classroom teacher").delete()
        Contact.objects.get(client_id="clatea19010101").delete()
        Contact.objects.get(client_id="stuuse19010101").delete()
        Contact.objects.get(client_id="voluse19010101").delete()
        Account.objects.get(name="Test_Org").delete()
        self.assertEqual(response.url, reverse("staff"))
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)

    def test_create_classroom_invalid_form(self):
        self.client.force_login(self.create_staff_user())
        response = self.client.post(reverse("create_classroom"), {})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_class_offering(self):
        self.client.force_login(self.create_staff_user())
        response = self.client.get(reverse("create_class_offering"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTemplateUsed(response, "create_class_offering.html")
        response = self.client.post(
            reverse("create_class_offering"), self.valid_create_class_offering_form()
        )
        ClassOffering.objects.get(name="Summer 2019 - Android - Test_Org - M/W - classroom teacher").delete()
        Account.objects.get(name="Test_Org").delete()
        self.assertEqual(response.url, reverse("staff"))
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)

    def test_create_class_offering_invalid_form(self):
        self.client.force_login(self.create_staff_user())
        response = self.client.post(reverse("create_class_offering"), {})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_make_announcement(self):
        self.client.force_login(self.create_staff_user())
        response = self.client.get(reverse("make_announcement"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTemplateUsed(response, "make_announcement.html")
        response = self.client.post(
            reverse("make_announcement"), self.valid_make_announcement_form()
        )
        self.assertEqual(response.url, reverse("staff"))
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)

    def test_make_announcement_invalid_form(self):
        self.client.force_login(self.create_staff_user())
        response = self.client.post(reverse("make_announcement"), {})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_staff_user(self):
        self.client.force_login(self.create_staff_user())
        response = self.client.get(reverse("create_staff_user"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTemplateUsed(response, "create_staff_user.html")
        response = self.client.post(
            reverse("create_staff_user"), self.valid_create_user_form("staff")
        )
        Contact.objects.get(client_id="testes19010101").delete()
        self.assertEqual(response.url, reverse("staff"))
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.client.force_login(self.create_nonstaff_user())
        self.assertRaises(PermissionError)

    def test_create_staff_user_invalid_form(self):
        self.client.force_login(self.create_staff_user())
        response = self.client.post(reverse("create_staff_user"), {})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_teacher_user(self):
        self.client.force_login(self.create_staff_user())
        response = self.client.get(reverse("create_teacher_user"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTemplateUsed(response, "create_teacher_user.html")
        response = self.client.post(
            reverse("create_teacher_user"), self.valid_create_user_form("teacher")
        )
        Contact.objects.get(client_id="testes19010101").delete()
        self.assertEqual(response.url, reverse("staff"))
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.client.force_login(self.create_nonstaff_user())
        self.assertRaises(PermissionError)

    def test_create_teacher_user_invalid_form(self):
        self.client.force_login(self.create_staff_user())
        response = self.client.post(reverse("create_teacher_user"), {})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_student_user(self):
        self.client.force_login(self.create_staff_user())
        response = self.client.get(reverse("create_student_user"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTemplateUsed(response, "create_student_user.html")
        response = self.client.post(
            reverse("create_student_user"), self.valid_create_user_form("student")
        )
        Contact.objects.get(client_id="testes19010101").delete()
        self.assertEqual(response.url, reverse("staff"))
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.client.force_login(self.create_nonstaff_user())
        self.assertRaises(PermissionError)

    def test_create_student_user_invalid_form(self):
        self.client.force_login(self.create_staff_user())
        response = self.client.post(reverse("create_student_user"), {})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_volunteer_user(self):
        self.client.force_login(self.create_staff_user())
        response = self.client.get(reverse("create_volunteer_user"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTemplateUsed(response, "create_volunteer_user.html")
        response = self.client.post(
            reverse("create_volunteer_user"), self.valid_create_user_form("volunteer")
        )
        Contact.objects.get(client_id="testes19010101").delete()
        self.assertEqual(response.url, reverse("staff"))
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.client.force_login(self.create_nonstaff_user())
        self.assertRaises(PermissionError)

    def test_create_volunteer_user_invalid_form(self):
        self.client.force_login(self.create_staff_user())
        response = self.client.post(reverse("create_volunteer_user"), {})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
