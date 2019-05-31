from django.test import TestCase, RequestFactory
from staff.views import *
from tests.test_home_models import *
from home.forms import UserRegisterForm
from mixer.backend.django import mixer
from django.contrib.auth.models import User, AnonymousUser
from django.urls import reverse
from rest_framework import status

class StaffViewsTest(TestCase):

    def test_staff(self):
        request = RequestFactory().get(reverse('home-home'))
        request.user = HomeModelsTest.create_authenticated_user(self, email="test@email.com")
        response = staff(request)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        request.user = HomeModelsTest.create_authenticated_user(self, email="test@missionbit.com", role="staff")
        response = staff(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_management(self):
        request = RequestFactory().get(reverse('home-home'))
        request.user = HomeModelsTest.create_authenticated_user(self)
        response = user_management(request)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        request.user = HomeModelsTest.create_authenticated_user(self, email="test@missionbit.com", role="staff")
        response = user_management(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_staff_user(self):
        request = RequestFactory().get(reverse('home-home'))
        request.user = HomeModelsTest.create_authenticated_user(self)
        response = create_staff_user(request)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        request.user = HomeModelsTest.create_authenticated_user(self, email="test@missionbit.com", role="staff")
        response = create_staff_user(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_teacher_user(self):
        request = RequestFactory().get(reverse('home-home'))
        request.user = HomeModelsTest.create_authenticated_user(self)
        response = create_teacher_user(request)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        request.user = HomeModelsTest.create_authenticated_user(self, email="test@missionbit.com", role="staff")
        response = create_teacher_user(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_student_user(self):
        request = RequestFactory().get(reverse('home-home'))
        request.user = HomeModelsTest.create_authenticated_user(self)
        response = create_student_user(request)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        request.user = HomeModelsTest.create_authenticated_user(self, email="test@missionbit.com", role="staff")
        response = create_student_user(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_volunteer_user(self):
        request = RequestFactory().get(reverse('home-home'))
        request.user = HomeModelsTest.create_authenticated_user(self)
        response = create_volunteer_user(request)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        request.user = HomeModelsTest.create_authenticated_user(self, email="test@missionbit.com", role="staff")
        response = create_volunteer_user(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_my_account_staff(self): 
        request = RequestFactory().get(reverse('home-home'))
        request.user = HomeModelsTest.create_authenticated_user(self)
        response = my_account_staff(request)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        request.user = HomeModelsTest.create_authenticated_user(self, email="test@missionbit.com", role="staff")
        response = my_account_staff(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)   

