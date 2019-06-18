from django.test import TestCase, RequestFactory
from staff.views import *
from home.forms import UserRegisterForm
from mixer.backend.django import mixer
from django.contrib.auth.models import User, AnonymousUser
from django.urls import reverse
from rest_framework import status

class BaseTestCase(TestCase):

    def create_authenticated_staff_user(self):
        user = User.objects.create_user(
                username = 'testuser',
                email = 'test@email.com',
                first_name = 'testfirst',
                last_name = 'testlast',
                password = 'beautifulbutterfly125'
                )
        Group.objects.get_or_create(name='staff')
        staff_group = Group.objects.get(name = 'staff')
        staff_group.user_set.add(user)
        return user

    def create_authenticated_nonstaff_user(self):
        user = User.objects.create_user(
                username = 'otherstafftestuser',
                email = 'othertest@email.com',
                first_name = 'othertestfirst',
                last_name = 'othertestlast',
                password = 'beautifulbutterfly125'
                )
        Group.objects.get_or_create(name='student')
        student_group = Group.objects.get(name = 'student')
        student_group.user_set.add(user)
        return user

class StaffViewsTest(BaseTestCase):

    def test_staff(self):
        request = RequestFactory().get(reverse('home-home'))
        request.user = self.create_authenticated_nonstaff_user()
        response = staff(request)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        request.user = self.create_authenticated_staff_user()
        response = staff(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_management(self):
        request = RequestFactory().get(reverse('home-home'))
        request.user = self.create_authenticated_nonstaff_user()
        response = user_management(request)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        request.user = self.create_authenticated_staff_user()
        response = user_management(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_staff_user(self):
        request = RequestFactory().get(reverse('home-home'))
        request.user = self.create_authenticated_nonstaff_user()
        response = create_staff_user(request)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        request.user = self.create_authenticated_staff_user()
        response = create_staff_user(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_teacher_user(self):
        request = RequestFactory().get(reverse('home-home'))
        request.user = self.create_authenticated_nonstaff_user()
        response = create_teacher_user(request)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        request.user = self.create_authenticated_staff_user()
        response = create_teacher_user(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_student_user(self):
        request = RequestFactory().get(reverse('home-home'))
        request.user = self.create_authenticated_nonstaff_user()
        response = create_student_user(request)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        request.user = self.create_authenticated_staff_user()
        response = create_student_user(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_volunteer_user(self):
        request = RequestFactory().get(reverse('home-home'))
        request.user = self.create_authenticated_nonstaff_user()
        response = create_volunteer_user(request)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        request.user = self.create_authenticated_staff_user()
        response = create_volunteer_user(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_my_account_staff(self): 
        request = RequestFactory().get(reverse('home-home'))
        request.user = self.create_authenticated_nonstaff_user()
        response = my_account_staff(request)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        request.user = self.create_authenticated_staff_user()
        response = my_account_staff(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)   
