from django.test import TestCase, RequestFactory
from volunteer.views import *
from home.forms import UserRegisterForm
from mixer.backend.django import mixer
from django.contrib.auth.models import User, AnonymousUser
from django.urls import reverse
from rest_framework import status


class BaseTestCase(TestCase):
    def create_authenticated_volunteer_user(self):
        user = User.objects.create_user(
            username="testuser",
            email="test@email.com",
            first_name="testfirst",
            last_name="testlast",
            password="beautifulbutterfly125",
        )
        Group.objects.get_or_create(name="volunteer")
        vol_group = Group.objects.get(name="volunteer")
        vol_group.user_set.add(user)
        return user

    def create_authenticated_nonvolunteer_user(self):
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


class VolunteerViewsTest(BaseTestCase):
    def test_volunteer(self):
        request = RequestFactory().get(reverse("home-home"))
        request.user = self.create_authenticated_nonvolunteer_user()
        response = volunteer(request)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        request.user = self.create_authenticated_volunteer_user()
        response = volunteer(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
