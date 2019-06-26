from django.test import TestCase, RequestFactory
from home.views import *
from home.forms import UserRegisterForm
from mixer.backend.django import mixer
from django.contrib.auth.models import User, AnonymousUser, Group
from django.urls import reverse
from rest_framework import status
from django.contrib import messages
from django.contrib.messages.storage.fallback import FallbackStorage


class BaseTestCase(TestCase):
    def create_user(self):
        user = User.objects.create_user(
            username="testuser",
            email="test@email.com",
            first_name="testfirst",
            last_name="testlast",
            password="testpassword",
        )
        return user

    def create_valid_form(
        self,
        username="testuser2",
        email="test@email.com",
        firstname="test",
        lastname="user",
    ):
        return {
            "username": username,
            "email": email,
            "first_name": firstname,
            "last_name": lastname,
            "password1": "beautifulbutterfly125",
            "password2": "beautifulbutterfly125",
        }


class HomeViewsTest(BaseTestCase):
    def test_home_unauthenticated(self):
        request = RequestFactory().get(reverse("home-home"))
        request.user = AnonymousUser()
        response = home(request)
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)

    def test_home_authenticated_student(self):
        request = RequestFactory().get(reverse("home-home"))
        request.user = self.create_user()
        Group.objects.get_or_create(name="student")
        student_group = Group.objects.get(name="student")
        student_group.user_set.add(request.user)
        response = home(request)
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)

    def test_home_authenticated_staff(self):
        request = RequestFactory().get(reverse("home-home"))
        request.user = self.create_user()
        Group.objects.get_or_create(name="staff")
        student_group = Group.objects.get(name="staff")
        student_group.user_set.add(request.user)
        response = home(request)
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)

    def test_home_authenticated_teacher(self):
        request = RequestFactory().get(reverse("home-home"))
        request.user = self.create_user()
        Group.objects.get_or_create(name="teacher")
        student_group = Group.objects.get(name="teacher")
        student_group.user_set.add(request.user)
        response = home(request)
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)

    def test_home_authenticated_volunteer(self):
        request = RequestFactory().get(reverse("home-home"))
        request.user = self.create_user()
        Group.objects.get_or_create(name="volunteer")
        student_group = Group.objects.get(name="volunteer")
        student_group.user_set.add(request.user)
        response = home(request)
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)

    def test_home_user_has_no_group(self):
        request = RequestFactory().get(reverse("home-home"))
        request.user = self.create_user()
        response = home(request)
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)

    def test_home_user_is_tagged(self):
        request = RequestFactory().get(reverse("home-home"))
        request.user = self.create_user()
        request.GET._mutable = True
        request.GET["tag"] = "student"
        response = home(request)
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)

    def test_logout(self):
        self.client.force_login(
            User.objects.create_user(
                username="testuser", email="testuser.example.com", password="top_secret"
            )
        )
        response = self.client.get(reverse("home-logout"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.wsgi_request.user.is_authenticated, False)

    def test_login(self):
        request = RequestFactory().get(reverse("home-home"))
        request.user = mixer.blend(User)
        response = login(request)
        self.assertEqual(response.url, reverse("login"))
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)

    def test_register(self):
        request = RequestFactory().get(reverse("home-home"))
        request.user = mixer.blend(User)
        response = register(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_landing_page(self):
        request = RequestFactory().get(reverse("home-home"))
        response = landing_page(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_register_after_oauth(self):
        request = RequestFactory().get(reverse("home-home"))
        response = register_after_oauth(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_register_as_student(self):
        request = RequestFactory().get(reverse("home-home"))
        request.user = mixer.blend(User)
        response = register_as_student(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_register_as_student_post(self):
        request = RequestFactory().post(reverse("home-home"), self.create_valid_form())
        request.user = self.create_user()
        setattr(request, "session", "session")
        messages = FallbackStorage(request)
        setattr(request, "_messages", messages)
        Group.objects.get_or_create(name="student")
        response = register_as_student(request)
        self.assertEqual(
            User.objects.filter(first_name="test").first().first_name, "test"
        )
        self.assertEqual(response.url, reverse("login"))
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)

    def test_register_as_student_invalid_form(self):
        request = RequestFactory().post(reverse("home-home"), {})
        request.user = self.create_user()
        setattr(request, "session", "session")
        messages = FallbackStorage(request)
        setattr(request, "_messages", messages)
        response = register_as_student(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_register_as_volunteer(self):
        request = RequestFactory().get(reverse("home-home"))
        request.user = self.create_user()
        response = register_as_volunteer(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_register_as_volunteer_post(self):
        request = RequestFactory().post(reverse("home-home"), self.create_valid_form())
        request.user = self.create_user()
        setattr(request, "session", "session")
        messages = FallbackStorage(request)
        setattr(request, "_messages", messages)
        Group.objects.get_or_create(name="volunteer")
        response = register_as_volunteer(request)
        self.assertEqual(
            User.objects.filter(first_name="test").first().first_name, "test"
        )
        self.assertEqual(response.url, reverse("login"))
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)

    def test_register_as_volunteer_invalid_form(self):
        request = RequestFactory().post(reverse("home-home"), {})
        request.user = self.create_user()
        setattr(request, "session", "session")
        messages = FallbackStorage(request)
        setattr(request, "_messages", messages)
        response = register_as_volunteer(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
