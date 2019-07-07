from django.test import TestCase, RequestFactory, Client
from django.contrib.auth.models import User, AnonymousUser as DjangoUser, AnonymousUser
from django.contrib.auth import authenticate
from django.urls import reverse
from rest_framework import status
from django.contrib.messages.storage.fallback import FallbackStorage

from home.views import *


class BaseTestCase(TestCase):
    def setUp(self) -> None:
        Group.objects.create(name="student")
        Group.objects.create(name="teacher")
        Group.objects.create(name="volunteer")
        Group.objects.create(name="donor")
        Group.objects.create(name="staff")

    def create_user(self):
        DjangoUser.objects.create_user(
            username="testuser",
            email="test@email.com",
            first_name="testfirst",
            last_name="testlast",
            password="testpassword",
        )
        test_user = authenticate(username="testuser", password="testpassword")
        return test_user

    def create_user_change_pwd(self):
        test_user = self.create_user()
        test_user.userprofile.change_pwd = True
        return test_user

    def create_user_in_group(self, group):
        test_user = self.create_user()
        self.add_user_to_group(test_user, group)
        return test_user

    def create_user_with_tag(self, tag):
        test_user = self.create_user()
        setattr(test_user, "tag", str(tag))
        return test_user

    def add_user_to_group(self, user, group):
        add_to_group = Group.objects.get(name=group)
        add_to_group.user_set.add(user)

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
            "password1": "top_secret_123",
            "password2": "top_secret_123",
        }

    def create_change_pwd_form(self):
        return {
            "old_password": "testpassword",
            "new_password1": "new_testpassword123",
            "new_password2": "new_testpassword123",
        }


class HomeViewsTest(BaseTestCase):

    def test_home_unauthenticated(self):
        request = RequestFactory().get(reverse("home-home"))
        request.user = AnonymousUser()
        response = home(request)
        response.client = Client()
        self.assertRedirects(response=response,
                             expected_url=reverse('home-landing_page')+'?next=/home/',
                             status_code=302,
                             target_status_code=200)

    def test_home_authenticated_student(self):
        self.client.force_login(self.create_user_in_group("student"))
        response = self.client.get(reverse("home-home"))
        self.assertRedirects(response=response,
                             expected_url='/student/',
                             status_code=302,
                             target_status_code=200)

    def test_home_authenticated_staff(self):
        self.client.force_login(self.create_user_in_group("staff"))
        response = self.client.get(reverse("home-home"))
        self.assertRedirects(response=response,
                             expected_url='/staff/',
                             status_code=302,
                             target_status_code=200)
    
    def test_home_authenticated_teacher(self):
        self.client.force_login(self.create_user_in_group("teacher"))
        response = self.client.get(reverse("home-home"))
        self.assertRedirects(response=response,
                             expected_url='/teacher/',
                             status_code=302,
                             target_status_code=200)

    def test_home_authenticated_volunteer(self):
        self.client.force_login(self.create_user_in_group("volunteer"))
        response = self.client.get(reverse("home-home"))
        self.assertRedirects(response=response,
                             expected_url='/volunteer/',
                             status_code=302,
                             target_status_code=200)

    def test_home_authenticated_donor(self):
        self.client.force_login(self.create_user_in_group("donor"))
        response = self.client.get(reverse("home-home"))
        self.assertRedirects(response=response,
                             expected_url='/donor/',
                             status_code=302,
                             target_status_code=200)

    def test_home_user_has_no_group(self):
        self.client.force_login(self.create_user())
        response = self.client.get(reverse("home-home"))
        self.assertRedirects(response=response,
                             expected_url='/register_after_oauth/',
                             status_code=302,
                             target_status_code=200)

    def test_home_change_pwd(self):
        self.client.force_login(self.create_user_change_pwd())
        response = self.client.get(reverse("home-home"))
        self.assertRedirects(response=response,
                             expected_url='/change_pwd/',
                             status_code=302,
                             target_status_code=200)

    def test_logout(self):
        self.client.force_login(
            DjangoUser.objects.create_user(
                username="testuser", email="testuser.example.com", password="top_secret"
            )
        )
        response = self.client.get(reverse("home-logout"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.wsgi_request.user.is_authenticated, False)

    def test_login(self):
        response = login(RequestFactory())
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)

    def test_register(self):
        response = self.client.get(reverse("home-register"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_landing_page(self):
        response = self.client.get(reverse("home-landing_page"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_register_as_student(self):
        response = self.client.get(reverse("home-register_as_student"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_change_pwd(self):
        self.client.force_login(self.create_user_change_pwd())
        response = self.client.post(reverse("change_pwd"), self.create_change_pwd_form())
        self.assertEqual(response.url, reverse("home-home"))
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        response = self.client.post(reverse("change_pwd"), {})
        self.assertTemplateUsed(response, template_name="home/change_pwd.html")

    def test_register_after_oauth(self):
        self.client.force_login(self.create_user())
        response = self.client.post(reverse("home-register_after_oauth"), {"role": "student"})
        self.assertEqual(response.url, reverse("home-home"))
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        response = self.client.post(reverse("home-register_after_oauth"), {"role": "volunteer"})
        self.assertEqual(response.url, reverse("home-home"))
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)

    def test_register_as_student_post(self):
        request = RequestFactory().post(reverse("home-home"), self.create_valid_form())
        request.user = self.create_user()
        setattr(request, "session", "session")
        messages = FallbackStorage(request)
        setattr(request, "_messages", messages)
        Group.objects.get_or_create(name="student")
        response = register_as_student(request)
        self.assertEqual(
            DjangoUser.objects.filter(first_name="test").first().first_name, "test"
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
        response = self.client.get(reverse("home-register_as_volunteer"))
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
            DjangoUser.objects.filter(first_name="test").first().first_name, "test"
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

    def test_register_as_donor(self):
        response = self.client.get(reverse("home-register_as_donor"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_register_as_donor_post(self):
        request = RequestFactory().post(reverse("home-home"), self.create_valid_form())
        request.user = self.create_user()
        setattr(request, "session", "session")
        messages = FallbackStorage(request)
        setattr(request, "_messages", messages)
        Group.objects.get_or_create(name="donor")
        response = register_as_donor(request)
        self.assertEqual(
            DjangoUser.objects.filter(first_name="test").first().first_name, "test"
        )
        self.assertEqual(response.url, reverse("login"))
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)

    def test_register_as_donor_invalid_form(self):
        request = RequestFactory().post(reverse("home-home"), {})
        request.user = self.create_user()
        setattr(request, "session", "session")
        messages = FallbackStorage(request)
        setattr(request, "_messages", messages)
        response = register_as_donor(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
