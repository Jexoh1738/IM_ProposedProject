from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse


class LoginScreenTests(TestCase):
    def test_valid_login_redirects_to_profile(self):
        User.objects.create_user(
            username="student@example.com",
            email="student@example.com",
            password="safe-password-123",
            first_name="Student",
        )

        response = self.client.post(
            reverse("login"),
            {"email": "student@example.com", "password": "safe-password-123"},
        )

        self.assertRedirects(response, reverse("profile"))
