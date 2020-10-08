from django.urls import reverse
from rest_framework.test import APITestCase

from users_module.models import User


class TestSetup(APITestCase):

    def setUp(self):
        self.register_url = reverse('rest_register')
        self.set_keyword_url = reverse('youtube-set-keyword')
        self.get_video_data_url = reverse('youtube-list')

        self.user_registration_data = {
            'email': 'email@gmail.com',
            "password1": 'password1234',
            "password2": 'password1234',
            "first_name": "User",
            "last_name": "Test",
        }

        self.user_data = {
            'email': 'email@gmail.com',
            "password": 'password1234',
        }

        self.keyword = {
            "value": "football"
        }

        return super().setUp()

    def authenticate(self):
        self.client.post(self.register_url, self.user_registration_data, format="json")
        user = User.objects.get(email=self.user_data.get('email'))
        self.client.force_authenticate(user=user)

    def tearDown(self):
        return super().tearDown()
