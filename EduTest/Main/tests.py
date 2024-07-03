from django.test import TestCase

from .models import Profile
from django.contrib.auth.models import User
from django.urls import reverse
# Create your tests here.


class HomePageViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testuserhomepage')
        self.profile = Profile.objects.create(user=self.user, access=2)

    def test_home_view_with_authenticated_user(self):
        self.client.login(username='testuser', password='testuserhomepage')

        response = self.client.get(reverse('Main:home'))

        self.assertEqual(response.status_code, 200)

        self.assertTrue(response.context['user_authorized'])
        self.assertEqual(response.context['access'], 2)

    def test_home_view_with_unauthorized_user(self):
        response = self.client.get(reverse('Main:home'))

        self.assertEqual(response.status_code, 200)

        self.assertFalse(response.context['user_authorized'])
        self.assertEqual(response.context['access'], 0)
