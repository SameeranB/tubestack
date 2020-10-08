from django.test import TransactionTestCase
from django.urls import reverse
from rest_framework.test import APITestCase

from users_module.models import User


class TestSetup(APITestCase):

    def setUp(self):
        self.register_url = reverse('rest_register')
        self.login_url = reverse('rest_login')

        self.user_registration_data = {
            'email': 'email@gmail.com',
            "password1": 'password1234',
            "password2": 'password1234',
            "first_name": "User",
            "last_name": "Test"
        }

        self.user_data = {
            'email': 'email@gmail.com',
            # 'username': 'username1234',
            "password": 'password1234',
        }

        return super().setUp()

    def tearDown(self):
        return super().tearDown()


class TestModelSetup(TransactionTestCase):
    def setUp(self):
        self.user1 = User.objects.create(email="admin@gmail.com",
                                         first_name="test",
                                         last_name="admin"
                                         )
        self.user2 = User.objects.create(email="member@gmail.com",
                                         first_name="test",
                                         last_name="member"
                                         )

    def tearDown(self) -> None:
        return super().tearDown()
