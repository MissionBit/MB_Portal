from django.test import TestCase
from home.models import Users

class HomeViewsTest(TestCase):
	def create_user(self, username="testuser", email="test@email.com", firstname="test",
		lastname="user", role="student"):
		return Users.objects.create(username=username,
									email=email,
									first_name=firstname,
									last_name=lastname,
									role=role)

	def test_user_creation(self):
		t = self.create_user()
		self.assertTrue(isinstance(t, Users))