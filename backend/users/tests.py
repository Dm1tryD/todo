from django.urls import reverse
from rest_framework.test import APITestCase

from .models import CustomUser
from django.test import TestCase


class RegisterViewTest(TestCase):
    def setUp(self):
        self.register_url = reverse('register')
        self.user_data = {
            'email': 'testuser@gmail.com',
            'password': 'Secret23',
            'password2': 'Secret23',
        }

    def test_register_corretly(self):
        response = self.client.post(self.register_url, self.user_data, format='json')
        self.assertEqual(response.status_code, 201, 'User is not registered')
        email = self.user_data['email']
        self.assertTrue(CustomUser.objects.get(email=email), 'User is not added to the database')

    def test_register_without_password2(self):
        self.user_data.pop('password2')
        response = self.client.post(self.register_url, self.user_data, format='json')
        self.assertEqual(response.status_code, 400, 'User is registered without password2')

    def test_register_without_email(self):
        self.user_data.pop('email')
        response = self.client.post(self.register_url, self.user_data, format='json')
        self.assertEqual(response.status_code, 400, 'User is registered without email')


class LoginViewTest(APITestCase):

    def setUp(self):
        self.user = CustomUser.objects.create_user('testuser@gmail.com', 'Secret23')

    def test_login_user_corretly(self):
        self.assertTrue(self.client.login(email='testuser@gmail.com', password='Secret23'))

    def test_login_user_wrong_email(self):
        self.assertFalse(self.client.login(email='testuser', password='Secret23'))

    def test_login_user_wrong_password(self):
        self.assertFalse(self.client.login(email='testuser@gmail.com', password='Secret67'))