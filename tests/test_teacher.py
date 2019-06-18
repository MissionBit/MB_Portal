from django.test import TestCase, RequestFactory
from teacher.views import *
from tests.test_home_models import *
from home.forms import UserRegisterForm
from mixer.backend.django import mixer
from django.contrib.auth.models import User, AnonymousUser
from django.urls import reverse
from rest_framework import status

"""
class TeacherViewsTest(TestCase):
	
    def test_teacher(self):
        request = RequestFactory().get(reverse('home-home'))
        request.user = HomeModelsTest.create_authenticated_user(self, email="test@email.com")
        response = teacher(request)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        request.user = HomeModelsTest.create_authenticated_user(self, email="test@missionbit.com", role="teacher")
        response = teacher(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
	"""