from django.test import TestCase, RequestFactory
from home.models import Users
from home.views import *
from home.forms import UserRegisterForm
from mixer.backend.django import mixer
from django.contrib.auth.models import User, AnonymousUser
from django.urls import reverse
from rest_framework import status
from django.contrib import messages
from django.contrib.messages.storage.fallback import FallbackStorage

class HomeModelsTest(TestCase):
    
    def create_user(self, username="testuser", email="test@email.com", first_name="test",
        last_name="user", role="student"):
        return Users.objects.create(username=username,
                                    email=email,
                                    first_name=first_name,
                                    last_name=last_name,
                                    role=role)

    def create_valid_form(self, username="testuser", email="test@email.com", firstname="test",
    	lastname="user", role="student"):
    	return { "username" : username,
    	         "email" : email,
    	         "first_name" : firstname,
    	         "last_name" : lastname,
    	         "role" : role,
    	         "password1" : "testpass123",
    	         "password2" : "testpass123" }    

    def create_authenticated_user(self, username="testuser", email="test@email.com", firstname="test",
        lastname="user", role="student"):
        user = Users.objects.create(username=username,
                                    email=email,
                                    first_name=firstname,
                                    last_name=lastname,
                                    role=role)
        user.is_authenticated = True
        user.save()
        return user    	

    def test_create_valid_form(self):
        form =self.create_valid_form()
        self.assertTrue(isinstance(form, dict))
        self.assertEqual(form['email'], "test@email.com")

    def test_user_creation(self):
        test_user = self.create_user()
        self.assertTrue(isinstance(test_user, Users))

    def test_authenticated_user_creation(self):
    	test_user = self.create_authenticated_user()
    	self.assertTrue(isinstance(test_user, Users))
    	self.assertEqual(test_user.is_authenticated, True)