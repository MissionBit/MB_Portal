from django.test import TestCase, RequestFactory
from tests.test_home_models import *
from home.views import *
from home.forms import UserRegisterForm
from mixer.backend.django import mixer
from django.contrib.auth.models import User, AnonymousUser
from django.urls import reverse
from rest_framework import status
from django.contrib import messages
from django.contrib.messages.storage.fallback import FallbackStorage

class HomeViewsTest(TestCase):

    def test_home_unauthenticated(self):
        request = RequestFactory().get(reverse('home-home'))
        request.user = AnonymousUser()
        response = home(request)
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)

    def test_home_authenticated_student(self):
        request = RequestFactory().get(reverse('home-home'))
        request.user = HomeModelsTest.create_authenticated_user(self)
        response = home(request)
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)

    def test_home_authenticated_staff(self):
        request = RequestFactory().get(reverse('home-home'))
        request.user = HomeModelsTest.create_authenticated_user(self, role="staff")
        response = home(request)
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)

    def test_home_authenticated_teacher(self):
        request = RequestFactory().get(reverse('home-home'))
        request.user = HomeModelsTest.create_authenticated_user(self, role="teacher")
        response = home(request)
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)

    def test_home_authenticated_volunteer(self):
        request = RequestFactory().get(reverse('home-home'))
        request.user = HomeModelsTest.create_authenticated_user(self, role="volunteer")
        response = home(request)
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)

    def test_home_no_matching_user(self):
        request = RequestFactory().get(reverse('home-home'))
        request.user = mixer.blend(User)
        response = home(request)
        self.assertEqual(response.url, reverse('home-register_after_oauth'))
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)

    def test_logout(self):
        self.client.force_login(
            User.objects.create_user(
                username='testuser',
                email='testuser.example.com',
                password='top_secret'
            )
        )
        response = self.client.get(reverse('home-logout'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.wsgi_request.user.is_authenticated, False)

    def test_login(self):
        request = RequestFactory().get(reverse('home-home'))
        request.user = mixer.blend(User)
        response = login(request)
        self.assertEqual(response.url, reverse('login'))
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)

    def test_register(self):
        request = RequestFactory().get(reverse('home-home'))
        request.user = mixer.blend(User)
        response = register(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_landing_page(self):
        request = RequestFactory().get(reverse('home-home'))
        request.user = mixer.blend(User)
        response = landing_page(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_register_after_oauth(self):
        request = RequestFactory().get(reverse('home-home'))
        request.user = mixer.blend(User)
        response = register_after_oauth(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_register_as_student(self):
        request = RequestFactory().get(reverse('home-home'))
        request.user = mixer.blend(User)
        response = register_as_student(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_register_as_student_post(self):
        request = RequestFactory().post(reverse('home-home'), HomeModelsTest.create_valid_form(self, firstname="missionbit"))
        request.user = HomeModelsTest.create_authenticated_user(self)
        setattr(request, 'session', 'session')
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)
        self.assertEqual(Users.objects.count(), 1)
        response = register_as_student(request)
        self.assertEqual(Users.objects.count(), 2)
        self.assertEqual(Users.objects.filter(first_name = "missionbit").first().first_name, "missionbit")
        self.assertEqual(response.url, reverse('login'))
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)

    def test_register_as_student_invalid_form(self):
        request = RequestFactory().post(reverse('home-home'), { })
        request.user = mixer.blend(User)
        setattr(request, 'session', 'session')
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)
        response = register_as_student(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_register_as_volunteer(self):
        request = RequestFactory().get(reverse('home-home'))
        request.user = HomeModelsTest.create_user(self)
        response = register_as_volunteer(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_register_as_volunteer_post(self):
        request = RequestFactory().post(reverse('home-home'), HomeModelsTest.create_valid_form(self, firstname="missionbit",
        	role="volunteer"))
        request.user = HomeModelsTest.create_authenticated_user(self)
        setattr(request, 'session', 'session')
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)
        self.assertEqual(Users.objects.count(), 1)
        response = register_as_volunteer(request)
        self.assertEqual(Users.objects.count(), 2)
        self.assertEqual(Users.objects.filter(first_name = "missionbit").first().first_name, "missionbit")
        self.assertEqual(response.url, reverse('login'))
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)

    def test_register_as_volunteer_invalid_form(self):
        request = RequestFactory().post(reverse('home-home'), { })
        request.user = HomeModelsTest.create_user(self)
        setattr(request, 'session', 'session')
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)
        response = register_as_volunteer(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
